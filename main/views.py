from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.conf import settings
from main.models import  * # Reading, Branch, Device, Customer, Document
from main.helpers.snippets import total_energy, get_reading_stats, js_total_energy, js_get_reading_stats, format_date, js_get_readings, get_energy_usage
from main.helpers.datalogs import utility_vs_gen, daily_utility_vs_gen_kwh, get_last_readings
import json, datetime, calendar
from django.core.serializers.json import DjangoJSONEncoder
from main.helpers.fetch_readings import run_migrations
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
cache = {}

user_login_required = user_passes_test(lambda user: user.customer.is_main_admin, login_url='/auth/login')

def admin_customer_required(view_func):
    decorated_view_func = login_required(user_login_required(view_func))
    return decorated_view_func


def get_date_range():
        today = datetime.datetime.now()
        today_year = today.year
        today_month = today.month
        month_last_day = calendar.monthrange(today_year, today_month)[1]

        default_start_date = f"{today_year}/{today_month}/01"
        default_end_date = f"{today_year}/{today_month}/{month_last_day}"

        return default_start_date, default_end_date


def get_raw_range_for_js(add_one_day = False):
        if not add_one_day:
                today = datetime.datetime.now()
                today_year = today.year
                today_month = today.month
                month_last_day = calendar.monthrange(today_year, today_month)[1]

                default_start_date = f"{today_month}/01/{today_year}"
                default_end_date = f"{today_month}/{month_last_day}/{today_year}"

        if add_one_day:
                today = datetime.datetime.now()
                tommorrow = datetime.datetime.now() + datetime.timedelta(days = 1)
                today_year, today_month, today_day= today.year, today.month, today.day
                tommorrow_year, tommorrow_day, tommorrow_month = tommorrow.year, tommorrow.day, tommorrow.month

                default_start_date = f"{today_month}/{today_day}/{today_year}"
                default_end_date = f"{tommorrow_month}/{tommorrow.day}/{tommorrow_year}"

        return default_start_date, default_end_date

@login_required
def index(request):
        default_start_date, default_end_date = get_raw_range_for_js()

        page = "Dashboard"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)
        start_date, end_date = get_date_range()

        peak_kw, min_kw, avg_kw = "--", "--", "--" #get_reading_stats(user.id, start_date, end_date)
        energy_used = "loading.."#total_energy(user.id, default_start_date, default_end_date)

        return render(request, 'dashboard.html', {'user':user, "customer": customer, "branches": branches,"devices": devices, "page":page, "energy_used" : energy_used, "min_kw": min_kw, "peak_kw": peak_kw, "avg_kw": avg_kw, "def_start_date":default_start_date, "def_end_date":default_end_date})

@login_required
def power(request):
        page = "Power Readings (kW)"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)

        return render(request, 'power.html', {'user':user, "customer": customer, "page": page, "devices":devices})

@login_required
@admin_customer_required
def all_customers(request):
        page = "Customers"

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)
        customers = Customer.objects.all().order_by("-id")

        return render(request, 'all_customers.html', {'user':user, "customers": customers, "customer": customer, "page": page, "devices":devices})

@login_required
def view_customer(request, id):

        page = "Edit Profile"

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)
        customers = Customer.objects.all()

        edit_customer = Customer.objects.get(id = id)
        edit_branches = edit_customer.get_branches

        return render(request, 'edit_customer.html', {'user':user, "edit_customer": edit_customer, "edit_branches": edit_branches,  "customers": customers, "customer": customer, "page": page, "devices":devices, "branches": branches})

@login_required
def view_profile(request):

        page = "View Profile"

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)

        return render(request, 'view_profile.html', {'user':user, "customer": customer, "page": page, "devices":devices, "branches":branches})

@login_required
def last_read(request):
        
        page = "Last Readings"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)

        return render(request, 'last_read.html', {'user':user, "customer": customer, "page": page, "devices":devices})

@login_required
def voltage(request):
        page = "Voltage Readings (Volts)"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        return render(request, 'voltage.html', {'user':user, "customer": customer, "page": page})

@login_required
def current(request):
        page = "Current Readings (Amps)"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        return render(request, 'current.html', {'user':user, "customer": customer, "page": page})

@login_required
def readings(request):
        page = "Readings"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        devices = Device.objects.filter(user_id = request.user.id)
        start_date, end_date = get_raw_range_for_js(add_one_day=True)
        parameters = ["Current (Amps)", "Voltage (Volts)", "Active-Power (kW)", "Reactive-Power (kVAR)", "Energy (kWh)"]

        return render(request, 'readings.html', {'user':user, "customer": customer, "page": page, "devices":devices, "parameters":parameters, "def_start_date":start_date, "def_end_date":end_date})

@login_required
def energy_readings(request):
        page = "Energy Readings"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        devices = Device.objects.filter(user_id = request.user.id)
        start_date, end_date = get_raw_range_for_js(add_one_day=True)
        frequencies = ["15 Min.", "Hourly", "Daily", "Weekly"]

        return render(request, 'energy_readings.html', {'user':user, "customer": customer, "page": page, "devices":devices, "frequencies":frequencies, "def_start_date":start_date, "def_end_date":end_date})

@login_required
def readings_from_logs(request):
        page = "Readings"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        devices = Device.objects.filter(user_id = request.user.id)
        start_date, end_date = get_raw_range_for_js(add_one_day=True)
        parameters = ["Current (Amps)", "Voltage (Volts)", "Active-Power (kWh)", "Reactive-Power (kvar)", "Energy (kWH)"]

        return render(request, 'readings.html', {'user':user, "customer": customer, "page": page, "devices":devices, "parameters":parameters, "def_start_date":start_date, "def_end_date":end_date})

@login_required
def max_demand(request):
        page = "Max Demand (Amps)"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)    
        return render(request, 'max_demand.html', {'user':user, "customer": customer, "page": page})

@login_required
def score_card(request):
        page = "Score Card"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        device_id = request.POST.get("device", "")
        devices = Device.objects.filter(user__id = user.id) if device_id == "None" else Device.objects.filter(user = user)


        return render(request, 'score_card.html', {'user':user, "customer": customer, "page": page, "devices": devices})

@login_required
def messaging(request):

        page = "Messaging"
        user = User.objects.get(pk = request.user.id)

        customer = Customer.objects.get(user = user)
        customer.get_messages()
        conversation_partners = customer.get_conversation_partners()
        # print(conversation_partners)
        
        device_id = request.POST.get("device", "")
        devices = Device.objects.filter(user__id = user.id) if device_id == "None" else Device.objects.filter(user = user)

        return render(request, 'messaging.html', {'user':user, "customer": customer, "page": page, "devices": devices, "conversation_partners": conversation_partners})



###########################################################
###########################################################
#APISs SECTION
@login_required
def fetch_messages(request):
        user = User.objects.get(pk = request.user.id)
        
        customer = Customer.objects.get(user = user)
        messages = customer.get_messages()
        

        return HttpResponse(json.dumps({"response": "success", "data": messages}))

def send_message(request):
        user = User.objects.get(pk = request.user.id)
        

        if request.method == "POST":
                # print("REQUEST IS POST !!!")

                customer = Customer.objects.get(user = user)
                messages = customer.get_messages()
                data = json.loads(request.body)
                receiver = Customer.objects.get(id = data["customer_id"])
                text = data["text"]
                title = "no title"

                Message(sender = customer, receiver = receiver, description = title, content = text ).save()

                return HttpResponse(json.dumps({"response": "success", "data": messages}))

@login_required
def check_new_message(request):
        user = User.objects.get(pk = request.user.id)
        

        if request.method == "POST":
                # print("REQUEST IS POST !!!")

                customer = Customer.objects.get(user = user)
                conversation_partners = customer.get_conversation_partners()

                # print(conversation_partners)



# def fetch_vals_period(request):
#         #THIS IS SIMILAR TO THE (fetch_vals_period_per_device) FUNCTION ONLY THAT THIS FUNCTION ONLY FETCHES FOR ALL THE DEVICES I.E GETS OVERALL TOTAL FOR ALL DEVICES OF A CUSTOMER

#         user = User.objects.get(pk = request.user.id)
        
#         if request.method == "POST":

#                 branch_id = request.POST.get("device", "")
#                 devices = Device.objects.filter(user_id = request.user.id)
#                 start_date, end_date = request.POST.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
#                 #####REPLACE SLASHES WITH DASHES######
#                 start_date = format_date(start_date.replace("/","-"))
#                 end_date = format_date(end_date.replace("/","-"))

#                 user_cache = cache.get(user, False)

#                 if user_cache and  (datetime.datetime.now() - user_cache["lastlog"]).seconds < settings.CACHE_EXPIRY:
#                         data = user_cache["data"]
#                 else:

#                         peak_kw, min_kw, avg_kw = js_get_reading_stats(user.id, start_date, end_date)
#                         energy_used = js_total_energy(user.id, start_date, end_date)
                        
#                         utility_times, gen1_times, gen2_times = utility_vs_gen(devices, start_date, end_date)
                        
#                         devices = Device.objects.filter(user_id = request.user.id)
                        
#                         daily_device_usage = daily_utility_vs_gen_kwh(devices, start_date, end_date)

#                         data = {"peak_kw": peak_kw, "min_kw": min_kw, "avg_kw":avg_kw, "energy_used": energy_used, "gen1_times":gen1_times,"gen2_times":gen2_times, "utility_times":utility_times, "daily_device_usage":daily_device_usage}

#                         cache[user] = {"lastlog":datetime.datetime.now(), "data":data}

#         return HttpResponse(json.dumps({"response": "success", "data": data}))

def fetch_vals_period(request):
        #THIS IS SIMILAR TO THE (fetch_vals_period_per_device) FUNCTION ONLY THAT THIS FUNCTION ONLY FETCHES FOR ALL THE DEVICES I.E GETS OVERALL TOTAL FOR ALL DEVICES OF A CUSTOMER

        user = User.objects.get(pk = request.user.id)
        
        if request.method == "POST":

                data = json.loads(request.body)
                device_ids = data.get("device", "")
                devices = list(map(lambda id: Device.objects.get(id = id).device_id, device_ids))

                start_date, end_date = data.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
                #####REPLACE SLASHES WITH DASHES######
                start_date = format_date(start_date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))

                user_cache = cache.get(user, False)

                if 0==7 and user_cache and  (datetime.datetime.now() - user_cache["lastlog"]).seconds < settings.CACHE_EXPIRY:
                        data = user_cache["data"]
                else:
                        
                        utility_times, gen1_times, gen2_times = utility_vs_gen(devices, start_date, end_date)
                        
                        
                        daily_device_usage = daily_utility_vs_gen_kwh(devices, start_date, end_date)

                        data = {"gen1_times":gen1_times,"gen2_times":gen2_times, "utility_times":utility_times, "daily_device_usage":daily_device_usage}

                        cache[user] = {"lastlog":datetime.datetime.now(), "data":data}

        return HttpResponse(json.dumps({"response": "success", "data": data}))

def get_total_energy(request):

        if request.method == "POST":

                data = json.loads(request.body)

                device_ids = data.get("device", "")
                start_date, end_date = data.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
                print(start_date, end_date)
                #####REPLACE SLASHES WITH DASHES######

                start_date = format_date(start_date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))
                data = 0

                try:
                        for device_id in device_ids:

                                device = Device.objects.get(id = int(device_id))
                                raw_usage_dict = device.get_energy_this_month(start_date, end_date)  
                                data += raw_usage_dict["kwh_usage_so_far"]

                        return HttpResponse(json.dumps({"response": "success", "data": data}))
                
                except:
                        return HttpResponse(json.dumps({"response": "failure"}))
        else:
                return HttpResponse(json.dumps({"response": "failure", "message": "Bad Request"}))

def get_stats(request):

        if request.method == "POST":

                data = json.loads(request.body)

                device_ids = data.get("device", "")
                start_date, end_date = data.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
                #####REPLACE SLASHES WITH DASHES######

                start_date = format_date(start_date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))
                min_vals, max_vals, avg_vals = [], [], []

                try:
                        for device_id in device_ids:

                                device = Device.objects.get(id = int(device_id))
                                raw_usage_dict = device.get_min_max_power(start_date, end_date)[2] 
                                avg_read, max_read, min_read = raw_usage_dict["avg_read"], raw_usage_dict["max_read"], raw_usage_dict["min_read"]
                                min_vals.append(min_read)
                                max_vals.append(max_read)
                                avg_vals.append(avg_read)

                        min_vals, max_vals, avg_vals = min(min_vals), max(max_vals), (sum(avg_vals)/len(avg_vals))      
                        data = dict(min = min_vals, max = max_vals, avg = avg_vals)

                        return HttpResponse(json.dumps({"response": "success", "data": data}))
                
                except:
                        return HttpResponse(json.dumps({"response": "failure"}))
        else:
                return HttpResponse(json.dumps({"response": "failure"}))


def get_yesterday_today_usage(request):

        if request.method == "POST":

                user = User.objects.get(pk = request.user.id)
                data = json.loads(request.body)
                device_ids = data.get("devices", [])
                today_energy = yesterday_energy = 0

                now = datetime.datetime.now(tz = lagos_tz)
                yesterday_start = (now - datetime.timedelta(days = 1) ) - datetime.timedelta(hours = now.hour)
                today_start = (now - datetime.timedelta(hours = now.hour))
                end_date = now + datetime.timedelta(days = 1)

                for id in device_ids:
                        device = Device.objects.get(id = id)
                        today_energy += device.get_energy_this_month(today_start, end_date)["kwh_usage_so_far"]

                        yesterday_energy += device.get_energy_this_month(yesterday_start, today_start)["kwh_usage_so_far"]

                
                return HttpResponse(json.dumps({"response": "success", "data":{"today_energy":today_energy, "yesterday_energy": yesterday_energy}}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

        else:
                return HttpResponse(json.dumps({"response": "failure", "messagae": "Request not Post"}))

def fetch_vals_period_per_device(request):
        #THIS IS SIMILAR TO THE (fetch_vals_period) FUNCTION ONLY THAT THIS FUNCTION ONLY FETCHES FOR ALL THE DEVICES I.E GETS VALUE FOR JUST ONE DEVICE OF A CUSTOMER ALTHOUGH IT STILL HAS THE ABILITY TO FETCH OVERALL TOTAL.

        user = User.objects.get(pk = request.user.id)

        if request.method == "POST":

                device_id = request.POST.get("device", "")
                devices = Device.objects.filter(id = device_id)
                start_date, end_date = request.POST.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
                #####REPLACE SLASHES WITH DASHES######
                start_date = format_date(start_date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))

        try:
                peak_kw, min_kw, avg_kw = js_get_reading_stats(user.id, start_date, end_date, device_id = device_id)
                energy_used = js_total_energy(user.id, start_date, end_date, device_id = device_id)
                
                utility_times, gen1_times, gen2_times = utility_vs_gen(devices, start_date, end_date)

                daily_device_usage = daily_utility_vs_gen_kwh(devices, start_date, end_date)                

                return HttpResponse(json.dumps({"response": "success", "data": {"peak_kw": peak_kw, "min_kw": min_kw, "avg_kw":avg_kw, "energy_used": energy_used, "gen1_times":gen1_times,"gen2_times":gen2_times, "utility_times":utility_times, "daily_device_usage" : daily_device_usage}}))
        
        except:
                return HttpResponse(json.dumps({"response": "failure"}))

def get_energy_readings(request):
        #THIS ENDPOINT GIVES READINGS FOR ENERGY CONSUMPTION CHART IN RESOLUTIONS OF DAILY, HOURLY OR MONTHLY.

        user = User.objects.get(pk = request.user.id)

        if request.method == "POST":

                device_id = request.POST.get("device", "")
                frequency = request.POST.get("frequency", "")
                devices = Device.objects.filter(id = device_id)

                if devices:
                        device = devices[0]
                else:
                        return HttpResponse(json.dumps({"response": "failure", "message" : "No device with such ID"}))

                start_date, end_date = request.POST.get("period", "").split("-")#SPLIT VALUES TO INDIVIDUAL DATES
                #####REPLACE SLASHES WITH DASHES######
                start_date = format_date(start_date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))
                device.fetch_energy_per_device(frequency, start_date, end_date)
        try:

                usage = device.fetch_energy_per_device(frequency, start_date, end_date)           

                return HttpResponse(json.dumps({"response": "success", "data": {"usage":usage}}))
        
        except:
                return HttpResponse(json.dumps({"response": "failure"}))
        
def get_last_read(request):

        user = User.objects.get(pk = request.user.id)

        if request.method == "POST":

                device = request.POST.get("device", "")
                device_id = Device.objects.get(id = device)
                
                last_read = get_last_readings(device_id = device_id)

                return HttpResponse(json.dumps({"response": "success", "data":last_read}))



##THIS FUNCTION GETS THE MINIMUM AND MAXIMUM VALUES FOR ALL DEVICES TO BE SHOWN ON THE BARGRAPH 

# def get_min_max_each_device(devices, start_date, end_date):
        
#         result = {"devices":[],"max_reads":[], "min_reads":[]}

#         for device in devices:

#                 readings = []

#                 readings = [x[0] for x in  list(js_get_readings(device.id, start_date, end_date, "total_kw")) if x[0] > 0]#UNWRAP TUPLES AND REMOVE INTEGER VALUES

#                 if len(readings) > 0:
#                         max_read = int(max(readings))
#                         min_read = int(min(readings))
#                 else:
#                         min_read = max_read = avg_read = 0


#                 result["devices"].append(device.name)
#                 result["max_reads"].append(max_read)
#                 result["min_reads"].append(min_read)
        
#         return result

def get_line_readings(request): 

        user = User.objects.get(pk = request.user.id)

        if request.method == "POST":

                device_id = request.POST.get("device", "")
                devices = Device.objects.filter(id = device_id)
                date = request.POST.get("date", "")
                #####REPLACE SLASHES WITH DASHES######
                date = format_date(date.replace("/","-"))

                end_date = date + datetime.timedelta(days = 1) #ADD ONE DAY TO DAY TO ENABLE FILTERING BY DURATION AS YOU CANNOT FILTER BY ONE DAY.

                raw_data = list(Reading.objects.filter(device = devices[0], post_datetime__range = (date, end_date)).defer('post_datetime','post_date').order_by('post_datetime').values())

                data = raw_data # map(lambda __date: __date.strftime("%I:%M %p"))


        try:
                return HttpResponse(json.dumps({"response": "success", "data": data}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
        except:
                return HttpResponse(json.dumps({"response": "failure"}))

def get_line_readings_log(request): #READINGS FOR LINE CHARTS IN READINGS PAGE
        #THIS IS SIMILAR TO THE (get_line_readings) FUNCTION ONLY THAT THIS FUNCTION ONLY FETCHES FOR LOG TABLE

        user = User.objects.get(pk = request.user.id)

        if request.method == "POST":
                device_id = request.POST.get("device", "")
                devices = Device.objects.filter(id = device_id)
                date, end_date = request.POST.get("period", "").split("-") 

                #####REPLACE SLASHES WITH DASHES######
                date = format_date(date.replace("/","-"))
                end_date = format_date(end_date.replace("/","-"))

                raw_data = list(Reading.objects.filter(device = devices[0], post_datetime__range = (date, end_date)).defer('post_datetime','post_date').order_by('post_datetime').values())

                data = raw_data # map(lambda __date: __date.strftime("%I:%M %p"))

                for i in range(len(data)):
                        data[i]["post_datetime"] = data[i]["post_datetime"].strftime("%b. %d, %Y, %I:%M %p.")

        try:
                return HttpResponse(json.dumps({"response": "success", "data": data}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
        except:
                return HttpResponse(json.dumps({"response": "failure"}))


@login_required
def get_capacity_factors(request):
        user = User.objects.get(pk = request.user.id)
        
        response = Cache().get(f"get_capacity_factors-{user.id}")
        
        if response:
                return HttpResponse(json.dumps({"response": "success", "data":{"base_line":response}}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))
        branches = user.branch_set.all()
        response = []

        for branch in branches:

                devices = branch.device_set.all()

                for device in devices:
                        response.append({
                                "branch_name" : branch.name,
                                "branch_id" : branch.id,
                                "device_id": device.id,
                                "unique_id": device.device_id,
                                "capacity_factor": device.get_capacity_factor(),
                                "facility_energy_load_factor": device.get_facility_energy_load_factor(),
                                "baseline" : device.base_line_energy(),
                                "fuel_consumption": device.fuel_consumption(),
                                "total_kwh": device.get_total_kwh(),
                                "previous_scores" : device.get_previous_score()
                        })
        
        Cache().update(f"get_capacity_factors-{user.id}", response,)

        return HttpResponse(json.dumps({"response": "success", "data":{"base_line":response}}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))


#URL FOR POPULATING DATABASE
def load_datalogs(request):
        Datalog().populate()
        
        try:
                devices = Device.objects.all()
                acceptable_hours = [5, 6, 12, 18, 23]
                
                for device in devices:
                        current_hour = (datetime.datetime.now().hour)-12 # CONVERT TO 12 HOUR

                        if  current_hour in acceptable_hours:
                                device.check_load_balance()

                return HttpResponse(json.dumps({"response": "success"}))
                        
        except:
                return HttpResponse(json.dumps({"response": "failure", "message": "Something went wrong"}))

def load_readings(request):
        
        run_migrations()
        try:
                # run_migrations()

                return HttpResponse(json.dumps({"response": "success"}))
                        
        except:
                return HttpResponse(json.dumps({"response": "failure", "message": "Something went wrong"}))

@csrf_exempt
def update_historic_scores(request):

        devices = Device.objects.all()                        

        for device in devices:
                device.populate_previous_scores()

        return HttpResponse(json.dumps({"response": "success", "data":{"base_line":"response"}}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))

###########################################################
###########################################################
############## LOAD NEW CDD ###############################

@csrf_exempt
def upload_cdd(request):

        if request.method == 'POST':
                
                file = request.FILES.get("file")
                data = file.readlines()
                
                was_successful = Degree_Day.add_values(data)

                if was_successful:

                        return HttpResponse(json.dumps({"response": "success", "message": f"added {len(data)} new cdds'"}))
                else:
                        return HttpResponse(json.dumps({"response": "failure", "message": f"unable to add cdds'"}))
        else:
                        # return HttpResponse(json.dumps({"response": "error", "message": "Bad request"}))

                page = "Add Degree Days"
                user = User.objects.get(pk = request.user.id)

                customer = Customer.objects.get(user = user)
                
                device_id = request.POST.get("device", "")
                devices = Device.objects.filter(user__id = user.id) if device_id == "None" else Device.objects.filter(user = user)

                return render(request, 'add_cdd.html', {'user':user, "customer": customer, "page": page, "devices": devices})

@login_required
def upload_image(request):

        user = User.objects.get(id = request.user.id)
        customer_id = request.POST.get("customer_id", False)


        if request.method == 'POST':
                print("-------------------")
                file = request.FILES.get("file")

                if not customer_id:
                        customer = Customer.objects.get(user = user)
                        customer.image = file
                        customer.save()
                else:
                        customer = Customer.objects.get(id = customer_id)
                        customer.image = file
                        customer.save()


        return HttpResponse(json.dumps({"response": "success", "message": customer.image.url}))

@login_required
def update_details(request):

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        if request.method == 'POST':
                # # print(request.POST)
                company_name = request.POST.get("name")
                username = request.POST.get("username")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                customer.company_name = company_name
                customer.phone = phone
                customer.address = address

                try:
                        test_user = User.objects.get(username = username)

                        if not user.username == username:
                                return HttpResponse(json.dumps({"response": "user exists"}))

                except:
                        pass

                if any(not c.isalnum() for c in username):
                        return HttpResponse(json.dumps({"response": "failure"}))
                else:
                        user.username = username.lower()
                        customer.save()
                        user.save()

                        return HttpResponse(json.dumps({"response": "success"}))

        return HttpResponse(json.dumps({"response": "error"}))

@login_required
def update_branch(request):

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        if request.method == 'POST':
                # # print(request.POST)
                branch_name = request.POST.get("branch_name")
                address = request.POST.get("address")
                gen1 = request.POST.get("gen1")
                gen2 = request.POST.get("gen2")
                branch_id = request.POST.get("branch_id")

                branch = Branch.objects.get(id = branch_id)
                branch.name = branch_name
                branch.address = address
                branch.gen1_val = gen1
                branch.gen2_val = gen2

                branch.save()

                return HttpResponse(json.dumps({"response": "success"}))

        return HttpResponse(json.dumps({"response": "error"}))

@login_required
def create_branch(request):

        user = User.objects.get(pk = request.user.id)
        # customer = Customer.objects.get(user = user)

        if request.method == 'POST':
                # print(request.POST)
                branch_name = request.POST.get("branch_name")
                address = request.POST.get("address")
                gen1 = request.POST.get("gen1")
                gen2 = request.POST.get("gen2")
                customer_id = request.POST.get("customer_id")

                customer = Customer.objects.get(id = customer_id)

                branch = Branch(customer = customer, user = customer.user, name = branch_name, address = address, gen1_val = gen1, gen2_val = gen2)

                branch.save()

                return HttpResponse(json.dumps({"response": "success"}))

        return HttpResponse(json.dumps({"response": "error"}))

@login_required
def create_device(request):

        if request.method == 'POST':
                # # print(request.POST)
                device_name = request.POST.get("device_name")
                location = request.POST.get("location")
                device_id = request.POST.get("device_id")
                branch_id = request.POST.get("target_branch_id")

                branch = Branch.objects.get(id = branch_id)
                customer = branch.customer
                user = customer.user

                
                location = Location(name = location, branch = branch, customer = customer, user = user)
                location.save()
                device = Device(name = device_name, device_id = device_id, user = user, customer = customer, branch = branch, location = location)
                device.save()

                return HttpResponse(json.dumps({"response": "success"}))

        return HttpResponse(json.dumps({"response": "error"}))

@login_required
def update_device(request):

        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)

        if request.method == 'POST':
                # # print(request.POST)
                device_name = request.POST.get("device_name")
                location = request.POST.get("location")
                device_id = request.POST.get("device_id")
                device_pk = request.POST.get("device_pk")

                device = Device.objects.get(id = device_pk)
                device.name = device_name
                device_location = device.location
                device_location.name = location
                device.device_id = device_id

                device_location.save()
                device.save()

                return HttpResponse(json.dumps({"response": "success"}))

        return HttpResponse(json.dumps({"response": "error"}))

@login_required
def add_user(request):

        page = "Add User"
        user = User.objects.get(pk = request.user.id)
        customer = Customer.objects.get(user = user)
        branches = Branch.objects.filter(user_id = user.id)
        devices = Device.objects.filter(user_id = request.user.id)

        if request.method == 'POST':
                # # print(request.POST)
                company_name = request.POST.get("name")
                username = request.POST.get("username")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                customer.company_name = company_name
                customer.phone = phone
                customer.address = address

                try:
                        test_user = User.objects.get(username = username)

                        
                        return HttpResponse(json.dumps({"response": "user exists"}))

                except:
                        pass

                if any(not c.isalnum() for c in username):
                        return HttpResponse(json.dumps({"response": "failure"}))
                else:
                        username = username.lower()
                        new_user = User(username = username, email = "")
                        new_user.save()
                        new_user.set_password("12345678")
                        new_user.save()

                        customer = Customer(user = new_user, company_name = company_name, address = address, phone = phone)
                        customer.save()
                      

                        return HttpResponse(json.dumps({"response": "success"}))

        return render(request, 'add_user.html', {'user':user, "customer": customer, "page": page, "devices":devices})


@login_required
def edit_user(request):

        page = "Edit User"

        if request.method == 'POST':
                # # print(request.POST)
                company_name = request.POST.get("name")
                username = request.POST.get("username")
                phone = request.POST.get("phone")
                address = request.POST.get("address")
                customer_id = request.POST.get("customer_id")
                # print(customer_id)
                customer = Customer.objects.get(id = customer_id)
                user = customer.user

                customer.company_name = company_name
                customer.phone = phone
                customer.address = address

                
                try:
                        test_user = User.objects.get(username = username)

                        if not user.username == username:
                                return HttpResponse(json.dumps({"response": "user exists"}))

                except:
                        pass

                if any(not c.isalnum() for c in username):
                        return HttpResponse(json.dumps({"response": "failure"}))
                else:
                        user.username = username.lower()
                        customer.save()
                        user.save()

                        return HttpResponse(json.dumps({"response": "success"}))
        else:

                return HttpResponse(json.dumps({"response": "failure"}))


def simple_upload(request):

        # # print(type(request.FILES.get("file")))
        file = request.FILES.get("file")
        doc = Document(document = file)
        doc.save()
        if request.method == 'POST':
                # # print(request.POST)
                return HttpResponse(json.dumps({"response": "success", "message": doc.document.url}))
                
        return render(request, 'upload.html')