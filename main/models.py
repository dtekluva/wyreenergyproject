from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, Max, Min, Sum
from wyre.settings import lagos_tz
from main.helpers import get_baseline, remote_request, datalogs
from django.db.models.functions import Extract, ExtractMonth, ExtractYear
import datetime, math, json, pandas as pd, numpy as np
from django.conf import settings
from wyre.settings import BASE_DIR 
from django.utils.timezone import make_aware

number_of_months_for_base_line = 6

# Create your models here.
class Customer(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name    = models.CharField(max_length=56, default = " ",null=True, blank = True)
    phone           = models.CharField(max_length=40, default = 0,null=True, blank = True)
    address         = models.TextField(max_length=400, null=True, blank = True)
    image           = models.FileField(upload_to='customer_imgs/', default = 'avatar-6.jpg' ,null=True, blank = True) 
    is_main_admin   = models.BooleanField(default = False)
    is_bot          = models.BooleanField(default = False)
    added           = models.DateField(auto_now= True)

    def __str__(self):
        return f"{self.company_name} {self.id}"
    
    def get_device_count(self):
        return self.device_set.all().count()

    def get_branches(self):

        branches = self.branch_set.all()

        return branches

    def save(self,*args,**kwargs):

        super().save(*args,**kwargs)
        self.create_welcome_message()

    def get_conversation_partners(self):
        customers = self.message_sender.all() | self.message_receiver.all()

        conversations = []
        for message in customers:
            if message.receiver != self and message.receiver not in conversations:
                conversations.append(message.receiver)
            elif message.sender != self and message.sender not in conversations:
                conversations.append(message.sender)

        return conversations

    def get_messages(self):
        conversation_partners = self.get_conversation_partners()

        messages_dict = {}
        
        for conversation_partner in conversation_partners:

            messages = self.message_receiver.filter(sender = conversation_partner) | self.message_sender.filter(receiver = conversation_partner)
            self.message_receiver.filter(has_been_read = False).update(has_been_read = True) #MAKE UNREAD MESSAGES READ 
            messages = messages.order_by("id")

            formatted_messages = []
            for message in messages:

                formatted_messages.append({"id": message.id, "content":message.content, "read": message.has_been_read, "time":message.uploaded_at.strftime("%d %b %Y %H:%M:%S"), "outgoing": True if message.sender_id == self.id else False })

            messages_dict[conversation_partner.id] = formatted_messages

        return messages_dict

    def count_unread_messages(self):
        conversation_partners = self.get_conversation_partners()

        messages_dict = {}
        
        for conversation_partner in conversation_partners:

            messages = self.message_receiver.filter(has_been_read = False)

            num_of_messages = messages.count()

            return num_of_messages
        

    def create_welcome_message(self):

        try:
        
            sender = Customer.objects.get(is_main_admin = True)
            receiver = self
            if sender != receiver:
                text = f"Welcome {self.company_name}. !!"
                title = "Welcome message"

                Message(sender = sender, receiver = receiver, description = title, content = text ).save()
        except:
            pass

    def get_cached_score(self, value):

        response = Cache().get(key)

        return response

class Branch(models.Model):
    customer  = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    name      = models.CharField(max_length=256, default = " ",null=True, blank = True)
    phone     = models.CharField(max_length=40, default = 0,null=True, blank = True)
    address   = models.TextField(max_length=400, null=True, blank = True)
    gen1_val  = models.IntegerField(null=True, blank=True, default=0)
    gen2_val  = models.IntegerField(null=True, blank=True, default=0)


    def get_devices(self):
        devices = self.device_set.all()

        return devices

    class Meta:
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name


class Location(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    branch   = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user     = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    device_type = models.CharField(max_length=40, null=True, blank = True)
    name        = models.CharField(max_length=256, default = " ",null=True, blank = True)
    phone       = models.CharField(max_length=40, default = 0,null=True, blank = True)
    address     = models.TextField(max_length=400, null=True, blank = True)

    def __str__(self):
        return self.name


class Device(models.Model):
    customer        = models.ForeignKey(Customer, on_delete=models.CASCADE)
    location        = models.ForeignKey(Location, on_delete=models.CASCADE)
    branch          = models.ForeignKey(Branch, on_delete=models.CASCADE, default = 1)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    device_id       = models.CharField(max_length=40, null=True, blank = True)
    device_type     = models.CharField(max_length=40, null=True, blank = True)
    phone           = models.CharField(max_length=40, default = 0,null=True, blank = True)
    address         = models.TextField(max_length=400, null=True, blank = True)
    name            = models.CharField(max_length=100, null=True, blank = True)
    added           = models.DateField(auto_now= True)
    baseline        = models.IntegerField(null=True, blank=True, default=0)
    last_baseline_check = models.DateTimeField(default = "1999-01-01")
    previous_day_energy = models.IntegerField(null=True, blank=True, default=None)
    previous_day_energy_post_datetime = models.DateTimeField(default = datetime.datetime.now())
    last_load_balance_check           = models.DateTimeField(default = "1999-01-01")
    previous_score_last_update        = models.DateTimeField(default = "1999-01-01")


    def populate_previous_scores(self):

        scores = self.score_set.all().order_by("-date")
        max_previous_date = "2017-01-01"
        current_date = datetime.datetime.now()

        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month

        if not scores: 
            last_score = datetime.datetime.strptime(max_previous_date, '%Y-%m-%d')
        else:
            last_score = scores[0].date

        if last_score.year == current_date.year:

            date_range = [(last_score.year, month) for month in range(last_score.month, current_date.month)]
        
        else:

            date_range = []

            for year in range(last_score.year, current_year+1):

                if year == current_year:
                    new_date_range = [(current_date.year, month) for month in range(1, current_date.month)]

                elif year == last_score.year:
                    new_date_range = ([(year, month) for month in range(last_score.month, 13)])

                else:
                    new_date_range = ([(year, month) for month in range(1, 13)])

                date_range.extend(new_date_range)
        
        for year, month in date_range:

            is_already_calculated = bool(self.score_set.filter(date__year = year, date__month = month))

            if is_already_calculated:
                continue
            
            start_date_txt = f"{year}-{month}-01"
            end_date_txt   = f"{year}-{month}-{last_day_of_month(month)}"

            start_date = datetime.datetime.strptime(start_date_txt, '%Y-%m-%d')
            end_date   = datetime.datetime.strptime(end_date_txt, '%Y-%m-%d')

            fuel_consumption = self.fuel_consumption(start_date, end_date)
            total_kwh   = self.get_total_kwh(start_date, end_date)
            baseline    = self.base_line_energy_populate(start_date, end_date)
            felf        = self.get_min_max_power(start_date, end_date)

            
            device = self
            date   = end_date
            avg_load   = felf[2]["avg_read"] or 0
            peak_load  = felf[2]["max_read"] or 0
            fuel_consumption_gen1 = fuel_consumption["gen_1"] or 0
            fuel_consumption_gen2 = fuel_consumption["gen_2"] or 0
            hours_gen1            = fuel_consumption["gen_1_hrs"] or 0
            hours_gen2            = fuel_consumption["gen_2_hrs"] or 0
            baseline_energy       = baseline["forcasted_kwh_usage"] or 0
            energy_used           = baseline["kwh_usage_so_far"] or 0
            utility_kwh           = total_kwh["utility"] or 0
            gen1_kwh              = total_kwh["gen1"] or 0
            gen2_kwh              = total_kwh["gen2"] or 0

            Score(
                    device = device, date = date, avg_load = avg_load, peak_load  = peak_load, fuel_consumption_gen1 = fuel_consumption_gen1, fuel_consumption_gen2 = fuel_consumption_gen2, hours_gen1 = hours_gen1, hours_gen2  = hours_gen2, baseline_energy = baseline_energy, energy_used = energy_used, utility_kwh = utility_kwh, gen1_kwh = gen1_kwh, gen2_kwh = gen2_kwh
            ).save()



        {'kwh_usage_so_far': 0, 'number_of_days_so_far': 31, 'forcasted_kwh_usage': 0.0}
        {'unique_id': '128166', 
            'capacity_factor': 
                        { 
                        'gen1_capacity': 275, 
                        'gen2_capacity': 10,
                        'avg_load_gen_1': 116.71272443181822,
                        'avg_load_gen_2': None, 
                        'avg_load_total': 91.56223223782894, 'capacity_factor_gen_1': 0.42440990702479353, 'capacity_factor_gen_2': 0,'verdict_gen_1': 'perfect', 
                        'verdict_gen_2': 'perfect'
                        }, 
                        'facility_energy_load_factor': {
                                'factor_gen1': 0.5906245385170625, 
                                'factor_gen2': 0, 
                                'factor_total': 0.44413620736439496, 
                                'avg_load_total': 91.56223223782894, 
                                'max_load_total': 206.158, 
                                'remark': 'Fairly efficient - (Higher Is Better)'
                            },
                            'fuel_consumption': {
                                    'gen_1': 10424.32, 
                                    'gen_2': 0.0, 
                                    'gen_1_hrs': 265.25, 
                                    'gen_2_hrs': 0
                                }, 
                                'total_kwh': {
                                    'utility': 28630.0, 'gen1': 30841.0, 'gen2': 0
                                    }, 
                                'previous_scores': [{
                                    'id': 5, 'felf': 119.0,
                                    'avg_load': 32.0, 
                                    'peak_load': 68.0, 
                                    'capacity_factor_gen1': 7687.0, 
                                    'capacity_factor_gen2': 76.0, 
                                    'hours_gen1': 676.0, 
                                    'hours_gen2': 676.0, 
                                    'fuel_consumption_gen1': 657.0, 
                                    'fuel_consumption_gen2': 6576.0, 
                                    'baseline_energy': 56.0, 
                                    'energy_used': 567.0, 
                                    'utility_kwh': 0.0, 
                                    'gen1_kwh': 0.0, 
                                    'gen2_kwh': 0.0, 
                                    'month': 11, 
                                    'year': 2019
                                  }, {
                                      'id': 7, 
                                      'felf': 78.0, 
                                      'avg_load': 54.0, 
                                      'peak_load': 456.0, 
                                      'capacity_factor_gen1': 894.0, 
                                      'capacity_factor_gen2': 654.0, 
                                      'hours_gen1': 46648.0, 
                                      'hours_gen2': 4868.0, 
                                      'fuel_consumption_gen1': 896.0, 
                                      'fuel_consumption_gen2': 46870.0, 
                                      'baseline_energy': 4648.0, 
                                      'energy_used': 618.0, 
                                      'utility_kwh': 6.0, 
                                      'gen1_kwh': 4.0, 
                                      'gen2_kwh': 3.0, 
                                      'month': 10, 
                                      'year': 2019
                                      }
                                ]
                                }

        return True

    def get_previous_score(self):

        previous_scores = self.score_set.annotate(month = ExtractMonth('date'), year = ExtractYear('date')).order_by("-date").values("id", "month", "year", 'felf', "avg_load", "peak_load", "capacity_factor_gen1", "capacity_factor_gen2", "hours_gen1", "hours_gen2", "fuel_consumption_gen1", "fuel_consumption_gen2", "baseline_energy", "energy_used", "utility_kwh", "gen1_kwh", "gen2_kwh")
        
        response = list(previous_scores)[:5]

        return response

    def get_logs(self, start_date = False, end_date = False):
        
        result = {'resultCode': 200,
                    'message': None,
                    'data': []
                }

        # print(start_date, end_date)
        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day -1)-datetime.timedelta(days = now.hour))
        end_date = end_date or now - datetime.timedelta(days = 1)

        logs = self.datalog_set.filter(post_datetime__range = (start_date, end_date)).order_by("-post_datetime")
        # print(logs, (start_date, end_date))

        for log in logs:

            post_datetime = log.post_datetime.strftime("%Y-%m-%dT%H:%M:%S")
            digital_input_1 = log.digital_input_1
            digital_input_2 = log.digital_input_2
            digital_input_3 = log.digital_input_3
            digital_input_4 = log.digital_input_4
            summary_energy_register_1 = log.summary_energy_register_1
            summary_energy_register_2 = log.summary_energy_register_2
            total_kw = log.total_kw
            pulse_counter = log.pulse_counter

            log_dict = {'deviceID': self.device_id,
                    'recordTime': post_datetime,
                    'data': [
                        {'description': 'Digital Input #1',
                        'value': digital_input_1,
                        'units': '&nbsp;'},
                        {'description': 'Summary Energy Register #1',
                        'value': summary_energy_register_1,
                        'units': ''},
                        {'description': 'Summary Energy Register #2',
                        'value': summary_energy_register_2,
                        'units': ''},
                        {'description': 'Digital Input #2',
                        'value': digital_input_2,
                        'units': '&nbsp;'},
                        {'description': 'Total kW', 'value': total_kw, 'units': 'kW'},
                        {'description': 'Digital Input #3',
                        'value': digital_input_3,
                        'units': '&nbsp;'},
                        {'description': 'Digital Input #4',
                        'value': digital_input_4,
                        'units': '&nbsp;'},
                        {'description': 'Pulse counter #1', 'value': pulse_counter, 'units': '&nbsp;'}]}
            result['data'].append(log_dict)
            
        return result

    def get_logs_filtered(self, start_date = False, end_date = False):
        
        result = {'resultCode': 200,
                    'message': None,
                    'data': []
                }

        # print(start_date, end_date)
        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day -1)-datetime.timedelta(days = now.hour))
        end_date = end_date or now - datetime.timedelta(days = 1)

        logs = self.datalog_set.filter(post_datetime__range = (start_date, end_date)).order_by("-post_datetime").values("post_datetime", "total_kw", "summary_energy_register_1")
        # print(logs, (start_date, end_date))
            
        return logs

    def fetch_energy_per_device(self, frequency, start_date, end_date):

        data = self.get_logs(start_date, end_date)
        logs = datalogs.custom_energy_usage(data['data'], frequency)

        return logs 

    def get_total_kwh(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day-1))
        end_date = end_date or now

        data = datalogs.daily_utility_vs_gen_kwh([self.device_id], start_date, end_date)

        raw_daily_utility_values = data.get("utility", [])
        raw_daily_gen1_values = data.get("gen1", [])
        raw_daily_gen2_values = data.get("gen2", [])

        utility_kwh_sum = sum(raw_daily_utility_values)
        gen1_kwh_sum    = sum(raw_daily_gen1_values)
        gen2_kwh_sum    = sum(raw_daily_gen2_values)

        total_kwh = dict(utility = utility_kwh_sum, gen1 = gen1_kwh_sum, gen2 = gen2_kwh_sum)

        return total_kwh

    def get_min_max_power(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day-1))- datetime.timedelta(days = now.day)
        end_date = end_date or now

        aggregates_gen1 = self.datalog_set.filter(post_datetime__range = (start_date, end_date), digital_input_1 = 1).aggregate(
                avg_read=Avg('total_kw'),
                max_read=Max('total_kw'),
                min_read=Min('total_kw')
        )
        aggregates_gen2 = self.datalog_set.filter(post_datetime__range = (start_date, end_date), digital_input_1 = 2).aggregate(
                avg_read=Avg('total_kw'),
                max_read=Max('total_kw'),
                min_read=Min('total_kw')
        )
        aggregates_total = self.reading_set.filter(post_datetime__range = (start_date, end_date), total_kw__gte = 1 ).aggregate(
                avg_read=Avg('total_kw'),
                max_read=Max('max_sliding_window_kw_demand'),
                min_read=Min('total_kw')
        )

        return aggregates_gen1, aggregates_gen2, aggregates_total

    def get_capacity_factor(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = 30))
        end_date = end_date or now

        min_max_power = self.get_min_max_power(start_date = False, end_date = False, )

        avg_load_gen_1 = min_max_power[0]['avg_read']
        avg_load_gen_2 = min_max_power[1]['avg_read']
        avg_load_total = min_max_power[2]['avg_read']

        gen1_size = self.branch.gen1_val
        gen2_size = self.branch.gen2_val

        capacity_factor_gen1 = 0 if not gen1_size or not avg_load_gen_1 else avg_load_gen_1 / gen1_size
        capacity_factor_gen2 = 0 if not gen2_size or not avg_load_gen_2 else avg_load_gen_2 / gen2_size

        verdict_gen_1 = "overloaded" if capacity_factor_gen1 > 0.7 else "perfect"
        verdict_gen_2 = "overloaded" if capacity_factor_gen2 > 0.7 else "perfect"

        response =  {
                        "gen1_capacity" : gen1_size,
                        "gen2_capacity" : gen2_size,
                        "avg_load_gen_1": avg_load_gen_1,
                        "avg_load_gen_2": avg_load_gen_2,
                        "avg_load_total": avg_load_total,
                        "capacity_factor_gen_1": capacity_factor_gen1,
                        "capacity_factor_gen_2": capacity_factor_gen2,
                        "verdict_gen_1": verdict_gen_1,
                        "verdict_gen_2": verdict_gen_2
                    }
        return response
    
    def get_facility_energy_load_factor(self, start_date = False, end_date = False):

        avg_load_gen1, max_load_gen1 = self.get_min_max_power(start_date = False, end_date = False)[0]['avg_read'], self.get_min_max_power()[0]['max_read']

        avg_load_gen2, max_load_gen2 = self.get_min_max_power(start_date = False, end_date = False)[1]['avg_read'], self.get_min_max_power()[1]['max_read']
        
        avg_load_total, max_load_total = self.get_min_max_power(start_date = False, end_date = False)[2]['avg_read'], self.get_min_max_power()[2]['max_read']
        
        factor_gen1 = avg_load_gen1/max_load_gen1 if max_load_gen1 and avg_load_gen1 else 0
        factor_gen2 = avg_load_gen2/max_load_gen2 if max_load_gen2 and avg_load_gen2 else 0
        factor_total = avg_load_total/max_load_total if max_load_total and avg_load_total else 0

        remarks = {0: "Bad or No usage - (Higher Is Better)", 1: "Not so efficient - (Higher Is Better)", 2: "Fairly efficient - (Higher Is Better)", 3: "Reasonably efficient - (Higher Is Better)", 4: "Highly efficient - (Higher Is Better)"}

        remark_sigmoid = round(factor_total/0.25)  #ROUND LOAD FACTOR TO BETWEEN 0-1-2-3
        remark = remarks[remark_sigmoid]

        response =  {"factor_gen1" : factor_gen1, "factor_gen2" : factor_gen2, "factor_total" : factor_total, "avg_load_total": avg_load_total, "max_load_total": max_load_total, "remark": remark}
        
        return response

    def base_line_energy(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
       
        start_date = start_date or (now - datetime.timedelta(days = 30*number_of_months_for_base_line))
        end_date = end_date or datetime.datetime.now()

        if self.last_baseline_check.month != datetime.datetime.now().month:
        # if True:
            print("------ RECALCULATING BASELINE ------")
            start_year = start_date.year
            end_year = end_date.year

            #GET CURRENT MONTH CDD

            all_cdd_for_specified_month = Degree_Day.objects.filter(date__month=end_date.month)
            total_cdd = all_cdd_for_specified_month.count()
            avg_num_days_month = last_day_of_month(end_date.month)

            current_month_cdd = all_cdd_for_specified_month.aggregate(Sum("value")).get('value__sum')/round(total_cdd/avg_num_days_month)

            cdd = []
            months_kwh_data = []
            
            for year in range(start_year, end_year + 1):
                
                start_month = start_date.month
                end_month = start_date.month

                if start_year == end_year:
                    start_month = start_date.month 
                    end_month = end_date.month 

                elif year == start_year:
                    start_month = start_date.month
                    end_month = 13
                
                elif year == end_year :
                    start_month = 1
                    end_month = end_date.month

                for month in range(start_month, end_month):
                    cdd_aggregate = Degree_Day.objects.filter( date__year=year).filter( date__month=month).aggregate(Sum("value"))

                    # print(cdd_aggregate)
                    cdd.append(cdd_aggregate.get('value__sum'))
                    

                    kwh_set = (self.reading_set.filter( post_datetime__year=year).filter( post_datetime__month=month)).values("kwh_import")
                    
                    try:


                        kwh_month = kwh_set[len(kwh_set)-1].get("kwh_import", 0) - kwh_set[0].get("kwh_import", 0)
                    
                    except:

                        kwh_month = 0

                    months_kwh_data.append(kwh_month)

            prediction = get_baseline.predict_usage( months_kwh_data, cdd, current_month_cdd)

            current_usage_this_month = self.get_energy_this_month()
            current_usage_this_month["forcasted_kwh_usage"] = prediction

            self.baseline = prediction
            self.last_baseline_check = datetime.datetime.now()
            self.save()

        else:
            current_usage_this_month = self.get_energy_this_month()
            current_usage_this_month["forcasted_kwh_usage"] = self.baseline

        statistics = current_usage_this_month
        

        return statistics

    def base_line_energy_populate(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
       
        start_date = start_date 
        end_date = end_date or datetime.datetime.now()
        six_months_ago = (start_date - datetime.timedelta(days = 30*number_of_months_for_base_line))

        if six_months_ago.year == end_date.year:

            date_range = [(six_months_ago.year, month) for month in range(six_months_ago.month, end_date.month)]
        
        else:

            date_range = [(six_months_ago.year, month) for month in range(six_months_ago.month, 13)]
            date_range2 = [(end_date.year, month) for month in range(1, end_date.month)]

            date_range.extend(date_range2)

        


        if True:
            print("------ RECALCULATING BASELINE ------")
            start_year = six_months_ago.year
            end_year = end_date.year

            #GET CURRENT MONTH CDD

            all_cdd_for_specified_month = Degree_Day.objects.filter(date__month=end_date.month)
            total_cdd = all_cdd_for_specified_month.count()
            avg_num_days_month = last_day_of_month(end_date.month)

            current_month_cdd = all_cdd_for_specified_month.aggregate(Sum("value")).get('value__sum')/round(total_cdd/avg_num_days_month)

        #     print(current_month_cdd, total_cdd, avg_num_days_month )

            cdd = []
            months_kwh_data = []
            
            for year, month in date_range:  
                

                cdd_aggregate = Degree_Day.objects.filter( date__year=year).filter( date__month=month).aggregate(Sum("value"))

                cdd.append(cdd_aggregate.get('value__sum') or 0)
                    

                kwh_set = (self.reading_set.filter( post_datetime__year=year).filter( post_datetime__month=month)).values("kwh_import")

                kwh_month = (kwh_set[len(kwh_set)-1].get("kwh_import", 0) or 0) - (kwh_set[0].get("kwh_import", 0) or 0) if kwh_set else 0

                months_kwh_data.append(kwh_month)

            # print(cdd)
            # print(months_kwh_data)
            prediction = get_baseline.predict_usage( months_kwh_data, cdd, current_month_cdd)

            current_usage_this_month = self.get_energy_this_month(start_date , end_date)
            current_usage_this_month["forcasted_kwh_usage"] = prediction
            


        statistics = current_usage_this_month
        

        return statistics

    def get_energy_this_month(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day-1) ) - datetime.timedelta(hours = now.hour)
        end_date = end_date or now + datetime.timedelta(hours = now.hour)

        if isinstance(start_date, type(datetime.datetime.now())):
            start_date = date_only(start_date)

        if isinstance(end_date, type(datetime.datetime.now())):
            end_date = date_only(end_date)
        print("--------------------------------------", start_date, end_date)

        current_month_kwh_data = (self.datalog_set.filter(post_datetime__range = (start_date, end_date)).order_by("summary_energy_register_1"))
        print(current_month_kwh_data)
        
        try:

            start_kwh = current_month_kwh_data[0].summary_energy_register_1 or 0  #["summary_energy_register_1"]
            end_kwh = current_month_kwh_data.order_by('-id')[0].summary_energy_register_1 or 0

        except IndexError or AssertionError:
            start_kwh = 0
            end_kwh = 0

        kwh_usage = round(end_kwh - start_kwh)

        response = dict( kwh_usage_so_far = kwh_usage, number_of_days_so_far = now.day)

        return response

    def time_since_last_load_balance(self):

        hours = ((make_aware(datetime.datetime.now()) - self.last_load_balance_check).total_seconds())/3600

        return hours

    def check_load_balance(self):

        customer = self.customer
        admin    = Customer.objects.filter(is_bot = True)[0]
        now = datetime.datetime.now(tz = lagos_tz)

        start_date = now - datetime.timedelta(days = 6)
        end_date = now + datetime.timedelta(days = 1)

        current_month_kw = self.reading_set.filter(post_datetime__range = (start_date, end_date)).order_by("post_datetime")

        count = 0
        last_percentage_kw = 0

        imbalance_l1, imbalance_l2, imbalance_l3 = 0, 0, 0
        # print(self.time_since_last_load_balance())

        if self.time_since_last_load_balance() >= 1:

            for reading in current_month_kw:
                l1 = reading.kw_l1
                l2 = reading.kw_l2
                l3 = reading.kw_l3

                max_line_kw = max(l1, l2, l3)
                min_line_kw = min(l1, l2, l3)

                if not max_line_kw and not min_line_kw:
                    continue

                percentage_kw = (max_line_kw - min_line_kw)/max_line_kw

                if percentage_kw > 0.14:
                    count += 1

                    if percentage_kw > last_percentage_kw:
                        imbalance_l1, imbalance_l2, imbalance_l3 = l1, l2, l3
                        last_percentage_kw = percentage_kw

            if not (imbalance_l1 == imbalance_l2 == imbalance_l3 == 0):
                message = f"Cases of imbalance occured on {self.name} installed at {self.location}. Worst case <br>L1: {imbalance_l1}kw, <br>L2: {imbalance_l2}kw, <br>L3: {imbalance_l3}kw. <br>{round(last_percentage_kw*100)}% Imbalance."
                Message(sender = admin, receiver = customer, description = "", content = message ).save()
                print(message)
                self.save()
        
    def fuel_consumption(self, start_date = False, end_date = False):

        now = datetime.datetime.now(tz = lagos_tz)
        start_date = start_date or (now - datetime.timedelta(days = now.day-1))
        end_date = end_date or now + datetime.timedelta(days = 1)

        consumption_table = {
                            "0-10"   :  [0.9, 1.2, 1.7, 2.1], 
                            "11-12"  :  [1.0, 1.4, 2.1, 2.6], 
                            "13-15"  :  [1.3, 1.8, 2.6, 3.2], 
                            "16-20"  :  [1.7, 2.4, 3.5, 4.3], 
                            "21-25"  :  [2.1, 3.0, 4.3, 5.4], 
                            "26-30"  :  [2.6, 3.6, 5.2, 6.4], 
                            "31-40"  :  [3.4, 4.8, 7.0, 8.6], 
                            "41-50"  :  [4.3, 6.0, 8.6, 10.7], 
                            "51-75"  :  [6.4, 9.0, 12.7, 16.1], 
                            "76-100" : [8.3, 11.9, 16.1, 21.4], 
                            "101-150": [10.9, 17.3, 24.1, 32.1], 
                            "151-200": [14.1, 22.9, 32.7, 42.8], 
                            "200-250": [17.4, 28.6, 40.8, 53.5], 
                            "251-350": [23.7, 39.3, 56.0, 74.9], 
                            "351-500": [33.3, 55.6, 79.6, 107.0]
                            }

        keys = list(consumption_table.keys())

        capacity_factor = self.get_capacity_factor()

        gen1_cap = capacity_factor['gen1_capacity']
        gen2_cap = capacity_factor['gen2_capacity']
        load_factor_gen1 = capacity_factor["capacity_factor_gen_1"]
        load_factor_gen2 = capacity_factor["capacity_factor_gen_2"]
        
        gen_value_list = {"gen_1":(gen1_cap, load_factor_gen1), 
                          "gen_2": (gen2_cap, load_factor_gen2)}

        consumption = 0
        fuel_consumption = {"diesel_consumption":{"gen_1":0, "gen_2":0}}

        for gen in gen_value_list:
            gen_cap = gen_value_list[gen][0]
            load_factor = gen_value_list[gen][1]
        

            for key in keys:
                lower_bound, upper_bound = int(key.split("-")[0]), int(key.split("-")[1])
                key_range = range(lower_bound, upper_bound+1)

                if gen_cap in key_range:

                    consumption_list = consumption_table[key]

                    if load_factor <= 1 and load_factor > 0.75 or load_factor > 1: consumption_key = 3 
                    elif load_factor <= 0.75 and load_factor > 0.5: consumption_key = 2
                    elif load_factor <= 0.5 and load_factor > 0.25: consumption_key = 1
                    elif load_factor < 0.25: consumption_key = 0

                    consumption = consumption_list[consumption_key]

            fuel_consumption["diesel_consumption"][gen] = consumption
            # # print(fuel_consumption)

         
        utility, gen_1_hrs, gen_2_hrs = datalogs.process_usage(self.device_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

        
        fuel_consumption["diesel_consumption"]["gen_1"] = round(fuel_consumption["diesel_consumption"]["gen_1"] * gen_1_hrs, 2)
        fuel_consumption["diesel_consumption"]["gen_1_hrs"] = round(gen_1_hrs, 2)

        fuel_consumption["diesel_consumption"]["gen_2"] = round(fuel_consumption["diesel_consumption"]["gen_2"] * gen_2_hrs, 2)
        fuel_consumption["diesel_consumption"]["gen_2_hrs"] = round(gen_2_hrs, 2)

        return fuel_consumption["diesel_consumption"]

    def __str__(self):
        return self.device_id

@receiver(post_save, sender = Device)
def alert_customer(sender, **kwargs):
    device = kwargs['instance']
    

    date_time_str = '2017-01-01'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    customer = Customer.objects.get(user = device.user)

    Reading.objects.create(customer = customer, device = device, user = device.user, post_datetime =  date_time_obj, post_date = date_time_obj, post_time = date_time_obj)

    Datalog.objects.create(customer = customer, device = device, user = device.user, post_datetime = date_time_obj, post_date = date_time_obj, post_time = date_time_obj, digital_input_1 = 0, digital_input_2 = 0, digital_input_3 = 0, digital_input_4 = 0, summary_energy_register_1 = 0, summary_energy_register_2 = 0, total_kw = 0, pulse_counter = 0) 


class Reading(models.Model):
    customer      = models.ForeignKey(Customer, on_delete=models.CASCADE, default = 1)
    device        = models.ForeignKey(Device, on_delete=models.CASCADE, default = 1)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    post_datetime = models.DateTimeField(blank = True)
    post_date     = models.DateField(blank = True)
    post_time     = models.TimeField(blank=True)
    voltage_l1_l12  = models.FloatField(null=True, blank=True, default=0)
    voltage_l2_l23  = models.FloatField(null=True, blank=True, default=0)
    voltage_l3_l31  = models.FloatField(null=True, blank=True, default=0)
    current_l1      = models.FloatField(null=True, blank=True, default=0)
    current_l2      = models.FloatField(null=True, blank=True, default=0)
    current_l3      = models.FloatField(null=True, blank=True, default=0)
    kw_l1   = models.FloatField(null=True, blank=True, default=0)
    kw_l2   = models.FloatField(null=True, blank=True, default=0)
    kw_l3   = models.FloatField(null=True, blank=True, default=0)
    kvar_l1 = models.FloatField(null=True, blank=True, default=0)
    kvar_l2 = models.FloatField(null=True, blank=True, default=0)
    kvar_l3 = models.FloatField(null=True, blank=True, default=0)
    kva_l1  = models.FloatField(null=True, blank=True, default=0)
    kva_l2  = models.FloatField(null=True, blank=True, default=0)
    kva_l3  = models.FloatField(null=True, blank=True, default=0)
    power_factor_l1  = models.FloatField(null=True, blank=True, default=0)
    power_factor_l2  = models.FloatField(null=True, blank=True, default=0)
    power_factor_l3  = models.FloatField(null=True, blank=True, default=0)
    total_kw    = models.FloatField(null=True, blank=True, default=0)
    total_kvar  = models.FloatField(null=True, blank=True, default=0)
    total_kva   = models.FloatField(null=True, blank=True, default=0)
    total_pf    = models.FloatField(null=True, blank=True, default=0)
    avg_frequency   = models.FloatField(null=True, blank=True, default=0)
    neutral_current = models.FloatField(null=True, blank=True, default=0)
    volt_thd_l1_l12 = models.FloatField(null=True, blank=True, default=0)
    volt_thd_l2_l23 = models.FloatField(null=True, blank=True, default=0)
    volt_thd_l3_l31 = models.FloatField(null=True, blank=True, default=0)
    current_thd_l1  = models.FloatField(null=True, blank=True, default=0)
    current_thd_l2  = models.FloatField(null=True, blank=True, default=0)
    current_thd_l3  = models.FloatField(null=True, blank=True, default=0)
    current_tdd_l1  = models.FloatField(null=True, blank=True, default=0)
    current_tdd_l2  = models.FloatField(null=True, blank=True, default=0)
    current_tdd_l3  = models.FloatField(null=True, blank=True, default=0)
    kwh_import      = models.FloatField(null=True, blank=True, default=0)
    kwh_export      = models.FloatField(null=True, blank=True, default=0)
    kvarh_import    = models.FloatField(null=True, blank=True, default=0)
    kvah_total      = models.FloatField(null=True, blank=True, default=0)
    max_amp_demand_l1 = models.FloatField(null=True, blank=True, default=0)
    max_amp_demand_l2 = models.FloatField(null=True, blank=True, default=0)
    max_amp_demand_l3 = models.FloatField(null=True, blank=True, default=0)
    max_sliding_window_kw_demand   = models.FloatField(null=True, blank=True, default=0)
    accum_kw_demand    = models.FloatField(null=True, blank=True, default=0)
    max_sliding_window_kva_demand      = models.FloatField(null=True, blank=True, default=0)
    present_sliding_window_kw_demand    = models.FloatField(null=True, blank=True, default=0)
    present_sliding_window_kva_demand   = models.FloatField(null=True, blank=True, default=0)
    accum_kva_demand   = models.FloatField(null=True, blank=True, default=0)
    pf_import_at_maximum_kva_sliding_window_demand = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.post_date} customer-({self.customer})"


class Datalog(models.Model):
    customer      = models.ForeignKey(Customer, on_delete=models.CASCADE, default = 1)
    device        = models.ForeignKey(Device, on_delete=models.CASCADE, default = 1)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    post_datetime = models.DateTimeField(blank = True)
    post_date     = models.DateField(blank = True)
    post_time     = models.TimeField(blank=True)
    digital_input_1 = models.FloatField(null=True, blank=True, default=None)
    digital_input_2 = models.FloatField(null=True, blank=True, default=None)
    digital_input_3 = models.FloatField(null=True, blank=True, default=None)
    digital_input_4 = models.FloatField(null=True, blank=True, default=None)
    summary_energy_register_1 = models.FloatField(null=True, blank=True, default=None)
    summary_energy_register_2 = models.FloatField(null=True, blank=True, default=None)
    total_kw = models.FloatField(null=True, blank=True, default=None)
    pulse_counter = models.FloatField(null=True, blank=True, default=None)

    @staticmethod
    def filter_dict_from_list(data, value):
        
        for i in data['data']:
            # # print(i)
            if i['description'] == value:
                return (i['value'])
        return 0

    def populate(self):
        devices = Device.objects.all()

        for device in devices:
            # # print(device.device_id)
            print(device.device_id)
            if not ("125639" == device.device_id):
                continue
            device_last_read = Datalog.objects.filter(device = device).order_by("-post_datetime")


            if device_last_read:
                device_last_read_date = device_last_read[0].post_datetime
                device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")
            else:
                device_last_read_date = datetime.datetime.strptime("2018-01-01", "%Y-%m-%d")
                device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")

            print(device_last_read_date_str)
            end_date  = (device_last_read_date + datetime.timedelta(days = 15))
            end_date_str =  end_date.strftime("%Y-%m-%d")

            # # print(device_last_read_date_str, end_date_str)

            logs = False

            while not logs:

                
                logs = remote_request.make_remote_request(device_id = device.device_id, start_date = device_last_read_date_str, end_date = end_date_str)["data"]

                device_last_read_date = end_date
                device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")

                end_date  = (end_date + datetime.timedelta(days = 15))
                end_date_str =  end_date.strftime("%Y-%m-%d")

                print(device_last_read_date_str, end_date_str)

            for data in reversed(logs):
                
                # print(data)
                time = data['recordTime']
                time = make_aware(datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))
                
                d_i1 = self.filter_dict_from_list(data, "Digital Input #1")
                d_i2 = self.filter_dict_from_list(data, "Digital Input #2")
                d_i3 = self.filter_dict_from_list(data, "Digital Input #3")
                d_i4 = self.filter_dict_from_list(data, "Digital Input #4")
                summary_energy_register1 = self.filter_dict_from_list(data, "Summary Energy Register #1") or self.filter_dict_from_list(data, "kWh import")
                summary_energy_register2 = self.filter_dict_from_list(data, "Summary Energy Register #2")
                summary_energy_register3 = self.filter_dict_from_list(data, "Summary Energy Register #3")
                total_kW = self.filter_dict_from_list(data, "Total kW") or self.filter_dict_from_list(data, "Avg Total kW")
                pulse_counter = self.filter_dict_from_list(data, "Pulse counter #1")

                # print(time, d_i1, d_i2, d_i3, d_i4, summary_energy_register1, summary_energy_register2, total_kW,pulse_counter)
 
                # if not Datalog.objects.filter(post_datetime = time.strftime("%Y-%m-%d %H:%M:%S"), device__device_id = device.device_id):
                if not Datalog.objects.filter(post_datetime = time, device__device_id = device.device_id):

                    Datalog.objects.create(customer = device.customer, device = device, user = device.user, post_datetime = time, post_date = time, post_time = time, digital_input_1 = d_i1, digital_input_2 = d_i2, digital_input_3 = d_i3, digital_input_4 = d_i4, summary_energy_register_1 = summary_energy_register1, summary_energy_register_2 = summary_energy_register2, total_kw = total_kW, pulse_counter = pulse_counter) 
                    
                else:
                    continue
    
    
    # def populate(self):
    #     devices = Device.objects.all()


    #     for device in devices:
    #         # # print(device.device_id)
    #         # print(device.name)
    #         device_last_read = Datalog.objects.filter(device = device).order_by("-post_datetime")

    #         # if device.device_id != "133929":continue

    #         if device_last_read:
    #             device_last_read_date = device_last_read[0].post_datetime
    #             device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")
    #         else:
    #             device_last_read_date = datetime.datetime.strptime("2018-01-01", "%Y-%m-%d")
    #             device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")

    #         end_date  = (device_last_read_date + datetime.timedelta(days = 15))
    #         end_date_str =  end_date.strftime("%Y-%m-%d")

    #         # print(device_last_read_date_str, end_date_str)
    #         # print("end_date : ", end_date)

    #         logs = False

    #         while not logs:

                
    #             logs = remote_request.make_remote_request(device_id = device.device_id, start_date = device_last_read_date_str, end_date = end_date_str)["data"]

    #             device_last_read_date = end_date
    #             device_last_read_date_str = device_last_read_date.strftime("%Y-%m-%d")

    #             end_date  = (end_date + datetime.timedelta(days = 15))
    #             end_date_str =  end_date.strftime("%Y-%m-%d")

    #             # # print(device_last_read_date_str, end_date_str)

    #         for data in reversed(logs):
                
    #             # print(data)
    #             time = data['recordTime']
    #             # print(time)
    #             time = make_aware(datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))
                
    #             d_i1 = self.filter_dict_from_list(data, "Digital Input #1")
    #             d_i2 = self.filter_dict_from_list(data, "Digital Input #2")
    #             d_i3 = self.filter_dict_from_list(data, "Digital Input #3")
    #             d_i4 = self.filter_dict_from_list(data, "Digital Input #4")
    #             summary_energy_register1 = self.filter_dict_from_list(data, "Summary Energy Register #1") or self.filter_dict_from_list(data, "kWh import")
    #             summary_energy_register2 = self.filter_dict_from_list(data, "Summary Energy Register #2")
    #             summary_energy_register3 = self.filter_dict_from_list(data, "Summary Energy Register #3")
    #             total_kW = self.filter_dict_from_list(data, "Total kW") or self.filter_dict_from_list(data, "Avg Total kW")
    #             pulse_counter = self.filter_dict_from_list(data, "Pulse counter #1")

    #             # print(time, d_i1, d_i2, d_i3, d_i4, summary_energy_register1, summary_energy_register2, total_kW,pulse_counter)
 
    #             # if not Datalog.objects.filter(post_datetime = time.strftime("%Y-%m-%d %H:%M:%S"), device__device_id = device.device_id):
    #             if not Datalog.objects.filter(post_datetime = time, device__device_id = device.device_id):

    #                 Datalog.objects.create(customer = device.customer, device = device, user = device.user, post_datetime = time, post_date = time, post_time = time, digital_input_1 = d_i1, digital_input_2 = d_i2, digital_input_3 = d_i3, digital_input_4 = d_i4, summary_energy_register_1 = summary_energy_register1, summary_energy_register_2 = summary_energy_register2, total_kw = total_kW, pulse_counter = pulse_counter) 
    #                 # print("adding")
                    
    #             else:
    #                 print("Continuing")
    #                 continue
            
    #         pseudo_end_date = end_date - datetime.timedelta(days = 16) #COMPENSATE FOR ADDED 15 DAYS IN "WHILE NOT LOGS - ABOVE" THIS DATE IS TO CREATE A ILLUSION OF THE LAST DATE FETCHED IN CASE EXPERTPOWER DID NOT RETURN ANY DATA

    #         if time < pseudo_end_date and pseudo_end_date < make_aware(datetime.datetime.now()):
    #             # print("end_date : ", pseudo_end_date, "|\ttime : ", time)

    #             Datalog.objects.create(customer = device.customer, device = device, user = device.user, post_datetime = pseudo_end_date, post_date = pseudo_end_date, post_time = pseudo_end_date, digital_input_1 = d_i1, digital_input_2 = d_i2, digital_input_3 = d_i3, digital_input_4 = d_i4, summary_energy_register_1 = summary_energy_register1, summary_energy_register_2 = summary_energy_register2, total_kw = total_kW, pulse_counter = pulse_counter)
    #             print("Second Adding")
                
    #         else:
    #             print("Second continuing")
    #             continue

    def __str__(self):
        return f"{self.post_date} customer-({self.customer})"


class Message(models.Model):
    sender      = models.ForeignKey(Customer, on_delete=models.CASCADE, default = 1, related_name= "message_sender")
    receiver    = models.ForeignKey(Customer, on_delete=models.CASCADE, default = 2, related_name= "message_receiver")
    description = models.CharField(max_length=255, blank=True)
    has_new_message = models.BooleanField(default = True)
    content     = models.TextField(max_length=2000, blank=True)
    document    = models.FileField(upload_to='message_files/', null=True, blank=True, default=None)
    uploaded_at = models.DateTimeField(auto_now_add= datetime.datetime.now)
    has_been_read = models.BooleanField(default = False)

    # def get_conversations(self, participant1):

    #     return None if not self.message_set.all().order_by("-id") else self.message_set.all().order_by("-id")[0]
    

class Degree_Day(models.Model):
    date   = models.DateField(null=True, blank=True)
    value  = models.FloatField(null=True, blank=True, default=0)

    @staticmethod
    def add_values(data):

        try:

            data.pop(0) # REMOVE HEADING R COLUMN NAME

            for line in data:
                line = (line.decode()).split(",")
                date = datetime.datetime.strptime(line[0], "%d/%m/%Y")
                Degree_Day(date = date, value = line[1]).save()

            
            return True
        except:
            return False


class Score(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default = 1)
    date   = models.DateField(null=True, blank=True)
    felf   = models.FloatField(null=True, blank=True, default=0)
    avg_load   = models.FloatField(null=True, blank=True, default=0)
    peak_load  = models.FloatField(null=True, blank=True, default=0)
    capacity_factor_gen1  = models.FloatField(null=True, blank=True, default=0)
    capacity_factor_gen2  = models.FloatField(null=True, blank=True, default=0)
    fuel_consumption_gen1 = models.FloatField(null=True, blank=True, default=0)
    fuel_consumption_gen2 = models.FloatField(null=True, blank=True, default=0)
    hours_gen1            = models.FloatField(null=True, blank=True, default=0)
    hours_gen2            = models.FloatField(null=True, blank=True, default=0)
    baseline_energy       = models.FloatField(null=True, blank=True, default=0)
    energy_used           = models.FloatField(null=True, blank=True, default=0)
    utility_kwh           = models.FloatField(null=True, blank=True, default=0)
    gen1_kwh              = models.FloatField(null=True, blank=True, default=0)
    gen2_kwh              = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return f"{self.device.device_id} customer-({self.date})"


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


def filter_dict_from_list(data, value):
    
    for i in data['data']:
        # # print(i)
        if i['description'] == value:
            return (i['value'])
    return 0

def last_day_of_month(any_month):

    date_time_str = f'2018-{any_month}-28'
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')

    next_month = date_time_obj.replace(day=28) + datetime.timedelta(days=4)  # this will never fail

    return (next_month - datetime.timedelta(days=next_month.day)).day


def date_only(date_object):
    return f"{date_object.year}-{date_object.month}-{date_object.day}"


class Cache():

    #MAKE SURE TO IMPORT BASE_DIR FROM SETTINGS
    CACHE_FILENAME = "cache.json"
    CACHE_FILE_DIR = BASE_DIR.replace("\\", "/") + "/" + CACHE_FILENAME 
    
    def read_data(self):

        try:
            file = open(self.CACHE_FILE_DIR, "r")
            json.loads(file.read())
            file.close()
        except :

            file = open(self.CACHE_FILE_DIR, "w")
            file.write(json.dumps({"key":"val"}))
            file.close()

        file = open(self.CACHE_FILE_DIR, "r")
        data = json.loads(file.read())

        return data
    
    def write_data(self, data):

        file = open(self.CACHE_FILE_DIR, "w")
        file.write(json.dumps(data))
        file.close()

        return True

    def update(self, key, value, timed  = False):

        data = self.read_data()
        data[key] = value
        self.write_data(data)

        print("Successfully cached")
        return {f"cached-{key}" : True}


    def get(self, key):

        data = self.read_data().get(key, [])

        return data





# def base_line_energy(self, start_date = False, end_date = False):

#         now = datetime.datetime.now(tz = lagos_tz)
#         start_date = start_date or (now - datetime.timedelta(days = 30*10))
#         end_date = end_date or (now - datetime.timedelta(days = datetime.datetime.now().day))


#         if self.last_baseline_check.month != datetime.datetime.now().month:
#             print("------ RECALCULATING BASELINE ------")
        
#             cdd = [(object.date.strftime("%Y-%m-%d"), object.value) for  object in list(Degree_Day.objects.all())]

#             months_kwh_data = self.reading_set.filter(post_datetime__range = (start_date, end_date))
            
#             rearranged_months_kwh_data = []

#             for data in months_kwh_data:
#                     rearranged_months_kwh_data.append((data.post_datetime.strftime('%m/%d/%Y'), data.kwh_import))

#             prediction = get_baseline.predict_usage( rearranged_months_kwh_data, cdd)

#             current_usage_this_month = self.get_energy_this_month()
#             current_usage_this_month["forcasted_kwh_usage"] = prediction

#             self.baseline = prediction
#             self.last_baseline_check = datetime.datetime.now()
#             self.save()

#         else:
#             current_usage_this_month = self.get_energy_this_month()
#             current_usage_this_month["forcasted_kwh_usage"] = self.baseline

#         statistics = current_usage_this_month
        

#         return statistics