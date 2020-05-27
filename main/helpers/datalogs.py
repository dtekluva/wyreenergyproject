import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from dateutil import parser
import numpy as np
import pandas as pd
from main import models 
from main.helpers import remote_request


def make_local_request(device_id, start_date = "2019-08-15", end_date = "2019-08-16", url = 'logs'):
    
    if not isinstance(start_date, str):
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")
        

    # req = requests.get('http://expertpowerplus.com:8080/api/Login?userName=ppl&pass=Wyre1234')

    # # # print(req)
    # auth_key_name = (list(req.cookies)[0]).name #get name of cookie unit used to be (.ASPXAUTH) chnaged to (form_p)
    # auth_key_value = dict(req.cookies).get(auth_key_name) #get actual cookie unit
    # cookie = {auth_key_name: auth_key_value}
    # # device_id = "128166" #2019-04-15

    # url_data_logs = f'http://www.expertpowerplus.com:8080/api/basic/{device_id}/Datalogs?startDate={start_date}&endDate={end_date}&datalogNum=1'

    # url_last_read = f'http://expertpowerplus.com:8080/api/basic/{device_id}/LastReading'

    # url = url_data_logs if url == "logs" else url_last_read

    # r = requests.get(url, cookies=cookie)
    # return r.json()
    device = models.Device.objects.get(device_id = device_id)
    response = device.get_logs(start_date, end_date)
    # print(response)
    return response

def get_time_dif(a, b):
    
    c = b - a
    hours = c.seconds/3600
    return hours


def format_date(date):###THIS FUNCTION CONVERTS DATE FROM DD-MM-YYY TO YYY-MM-DD

    datetime_object = parser.parse(date)

    return datetime_object


def process_usage(device_id, start_date, end_date):
    # print(start_date, end_date)
    data = make_local_request(device_id, start_date, end_date)
    
    try:
        readings = data['data'][0]['data']

    except IndexError:
        return (0, 0, 0)

    utility_times = []
    gen_times = []

    for readings in (data['data']):
        record_time = readings["recordTime"]
        digital_in = filter_dict_from_list(readings, "Digital Input #1")
        energy_1 = filter_dict_from_list(readings, "Summary Energy Register #1")
        energy_2 = filter_dict_from_list(readings, "Summary Energy Register #3")
        total_energy = filter_dict_from_list(readings, "Total kW")

        # # print(record_time, digital_in, energy_1, energy_2, total_energy)        
        
        if digital_in == 0:
            utility_times.append(record_time)
        elif digital_in == 1:
            gen_times.append(record_time)

    nums = data["data"].copy()
    nums.reverse()
    utility_hrs = []
    gen1_hrs = []
    gen2_hrs = []

    while len(nums) > 1:
        x,y = nums.pop(0), nums[0]
        
        x_di = x["data"][0]["value"]
        y_di = y["data"][0]["value"]
        x_time, y_time = format_date(x["recordTime"]), format_date(y["recordTime"])
        x_kwh, y_kwh = x["data"][1]["value"], y["data"][1]["value"]
        
        if x_di == 0 and y_di == 1 or y_di == 2:
            time_diff = get_time_dif(x_time, y_time)
            if y_di == 1:
                gen1_hrs.append(time_diff)
            
            elif y_di == 2:
                gen2_hrs.append(time_diff)

            
        elif x_di == 1 and y_di == 0:
            time_diff = get_time_dif(x_time, y_time)
            utility_hrs.append(time_diff)
            
            
        elif x_di == y_di == 1 or x_di == y_di == 2:
            time_diff = get_time_dif(x_time, y_time)
            if y_di == 1:
                gen1_hrs.append(time_diff)
            
            elif y_di == 2:
                gen2_hrs.append(time_diff)

        elif x_di == y_di == 0:
            time_diff = get_time_dif(x_time, y_time)
            utility_hrs.append(time_diff)
            
    # print(sum(utility_hrs), sum(gen1_hrs), sum(gen2_hrs))
    return(sum(utility_hrs), sum(gen1_hrs), sum(gen2_hrs))


        
def utility_vs_gen(device_ids, start_date, end_date):
    utility_times = 0
    gen1_times = 0
    gen2_times = 0

    for device_id in device_ids:
        utility, gen1_hrs, gen2_hrs = process_usage(device_id, start_date, end_date)
        gen1_times += gen1_hrs
        gen2_times += gen2_hrs
        utility_times += utility
    
    return utility_times, gen1_times, gen2_times

def rearrange_data(data):#
    df_data = {}
    previous_day = False
    current_day = False
    
    for item in data:
        day = format_date(item["recordTime"])
        current_day = day.day

        if df_data.get(day.day, False):
            df_data[day.day].append(item)

        else:
            df_data[day.day] = []
            df_data[day.day].append(item)

        if previous_day != current_day and previous_day:
            # # print(previous_day != current_day)
            # # print(previous_day)
            # # print(df_data.keys(), '\n\n\n')
            df_data[previous_day].append(item)

        previous_day = day.day

    return df_data

def get_daily_usage(data):
    
    utility_kwh = []
    gen1_kwh = []
    gen2_kwh = []

    nums = data.copy()
    nums.reverse()
    utility_hrs = []
    gen1_hrs = []
    gen2_hrs = []

    while len(nums) > 1:
        x,y = nums.pop(0), nums[0]
        
        x_di = x["data"][0]["value"]
        y_di = y["data"][0]["value"]
        x_time, y_time = format_date(x["recordTime"]), format_date(y["recordTime"])
        x_kwh, y_kwh = x["data"][1]["value"], y["data"][1]["value"]
        
        if x_di == 0 and y_di == 1 or y_di == 2:
            kwh_diff = y_kwh - x_kwh
            if y_di == 1:
                gen1_kwh.append(kwh_diff)

            elif y_di == 2:
                gen2_kwh.append(kwh_diff)

        elif x_di == 1 and y_di == 0:
            kwh_diff = y_kwh - x_kwh
            utility_kwh.append(kwh_diff)


        elif x_di == y_di == 1 or x_di == y_di == 2:
            kwh_diff = y_kwh - x_kwh
            if y_di == 1:
                gen1_kwh.append(kwh_diff)

            elif y_di == 2:
                gen2_kwh.append(kwh_diff)

        elif x_di == y_di == 0:
            kwh_diff = y_kwh - x_kwh
            utility_kwh.append(kwh_diff)
            
    return (sum(utility_kwh), sum(gen1_kwh), sum(gen2_kwh))
        
def custom_energy_usage(data, frequency):
    
    """
        THIS GIVES ENERGY USAGE IN CUSTOM FREQUENCIES LIKE HOURS, WEEKS, AND DAYS DEPENDING ON THE INPUT FREQUENCY PASSED TO THE FUNCTION I.E Daily, Hourly, Weekly.
    """

    kwh = []
    times = []

    nums = data.copy()
    nums.reverse()
    usage_vals = []


    while len(nums) > 1:

        x,y = nums.pop(0), nums[0]

        x_time, y_time = format_date(x["recordTime"]), format_date(y["recordTime"])

        x_kwh, y_kwh = x["data"][1]["value"], y["data"][1]["value"]

        kwh_diff = y_kwh - x_kwh

        kwh.append(kwh_diff)

        if frequency == "Hourly":
            times.append(f"{x_time.year}/{x_time.month}/{x_time.day} {x_time.hour}:00") # HOURLY

        elif frequency == "Daily":    
            times.append(f"{x_time.month}/{x_time.day}-{x_time.strftime('%A')[:3]}") # DAILY

        elif frequency == "Weekly":
            times.append(f"{x_time.year}, wk-{x_time.isocalendar()[1]}")# WEEKLY
        
        elif frequency == "15 Min.":
            times.append(f"{x_time.year}/{x_time.month}/{x_time.day} {x_time.hour}:{x_time.minute}")
    
    
    df = pd.DataFrame()
    df["kwh"] = kwh
    df["times"] = times
    
    grouped_data = df.groupby(by = "times", sort = False).sum().reset_index()

    return grouped_data.to_dict("list")


def daily_utility_vs_gen_kwh(device_ids, start_date, end_date):
    daily_data = {}
    daily_usage = {"days":[], "gen1":[], "gen2":[], "utility":[]}

    for device_id in device_ids:
        old_data = daily_data.copy()
        data = make_local_request(device_id, start_date, end_date)
        df_data = rearrange_data(data["data"])

        
        for day in df_data:
            if daily_data.get(day,False):
                daily_data[day] = get_daily_usage(df_data[day])
            else:
                daily_data[day] = []
                daily_data[day] = get_daily_usage(df_data[day])
                
        daily_data = merge_daily_readings(old_data, daily_data)

    for key in daily_data:
        daily_usage["days"].append(key)
        daily_usage["utility"].append(daily_data[key][0])
        daily_usage["gen1"].append(daily_data[key][1])
        daily_usage["gen2"].append(daily_data[key][2])

    daily_usage["days"], daily_usage["utility"], daily_usage["gen1"], daily_usage["gen2"] = sort_multiple_lists(daily_usage["days"], daily_usage["utility"], daily_usage["gen1"], daily_usage["gen2"]) #rearrange daily day accending

    return daily_usage


def merge_daily_readings(old_read, new_read):
    
    for key in new_read:
        old_value = old_read.get(key,(0,0,0))
        old_read[key] = [new_read[key][0] + old_value[0], new_read[key][1] + old_value[1], new_read[key][2] + old_value[2]]
    
    
    return old_read


def get_last_readings(device_id):

    template = {'voltage_l1_l12': {"value":0}, 'voltage_l2_l23': {"value":0}, 'voltage_l3_l31': {"value":0},
         'current_l1': {"value":0}, 'current_l2': {"value":0}, 'current_l3': {"value":0}, 'kw_l1': {"value":0}, 'kw_l2': {"value":0}, 
         'kw_l3': {"value":0}, 'kvar_l1': {"value":0}, 'kvar_l2': {"value":0}, 'kvar_l3': {"value":0}, 'kva_l1': {"value":0}, 
         'kva_l2': {"value":0}, 'kva_l3': {"value":0}, 'power_factor_l1': {"value":0}, 'power_factor_l2': {"value":0}, 'power_factor_l3': {"value":0}, 'total_kw': {"value":0}, 'total_kvar': {"value":0}, 'total_kva': {"value":0}, 
         'total_pf': {"value":0}, 'avg_frequency': {"value":0}, 'neutral_current': {"value":0}, 'volt_thd_l1_l12': {"value":0}, 'volt_thd_l2_l23': {"value":0}, 'volt_thd_l3_l31': {"value":0}, 'current_thd_l1': {"value":0}, 'current_thd_l2': {"value":0},
         'current_thd_l3': {"value":0}, 'current_tdd_l1': {"value":0}, 'current_tdd_l2': {"value":0}, 'current_tdd_l3': {"value":0},
         'kwh_import': {"value":0}, 'kwh_export': {"value":0}, 'kvarh_import': {"value":0}, 'kvah_total': {"value":0},
         'max_amp_demand_l1': {"value":0}, 'max_amp_demand_l2': {"value":0}, 'max_amp_demand_l3': {"value":0},
         'max_sliding_window_kw_demand': {"value":0}, 'accum_kw_demand': {"value":0},
         'max_sliding_window_kva_demand': {"value":0}, 'present_sliding_window_kw_demand': {"value":0},
         'present_sliding_window_kva_demand': {"value":0}, 'accum_kva_demand': {"value":0}, 
         'pf_import_at_maximum_kva_sliding_window_demand': {"value":0}}

    raw_data = remote_request.make_remote_request(device_id = device_id, url = "last_read")

    last_read = raw_data["data"][0]['data']
    template["record_time"] = raw_data["data"][0]["recordTime"]

    for value in last_read:
        template[value["description"].lower().replace('.','').replace(' ','_').replace('/','_').replace('(','').replace(')','')] = value
        
    return template

def sort_multiple_lists(i,j,k,l):
    """(i,j,k,l) are lists to be sorted"""
    try:
        sorted_list = list(sorted(zip(i,j,k,l)))
        i,j,k,l = zip(*sorted_list)
    except:
        i,j,k,l = [],[],[],[]

    return i,j,k,l
# daily_utility_vs_gen_kwh(["125639"], "2019-07-17", "2019-08-01")


def filter_dict_from_list(data, value):
        
        for i in data['data']:
            # # print(i)
            if i['description'] == value:
                return (i['value'])
        return 0
