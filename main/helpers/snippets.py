from main.models import Reading, Customer, Location, Reading, Device
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import pandas as pd
import json

def get_readings(device_id, start_date, end_date, target):
    start_date = "2019-07-01"
    end_date = "2019-07-30"

    device = device.objects.get(id = device_id)
    readings = Reading.objects.filter(device = device, post_datetime__range = (start_date, end_date)).values_list(target)
 
    return readings


def get_device_reading_for_period(start_date, end_date, device_id):#KWH_IMPORT
    start_date = "2019-07-01"
    end_date = "2019-07-30"
    device = device.objects.get(id = device_id)

    readings = Reading.objects.filter(device = device, post_datetime__range = (start_date, end_date)).order_by("post_datetime").values_list('kwh_import')

    if len(readings) != 0:

        total_kwh_device  = readings[len(readings)-1][0] - readings[0][0]
    
    else:

        return 0

    return total_kwh_device

def total_energy(user_id, start_date, end_date):#GETS THE ENERGY DIFFERENCE FROM A START DATE TO END DATE FOR A ALL DEVICES IN ALL LOCATIONS FOR A USER
    
    devices = Device.objects.filter(user__id = user_id)
    reading_collections = map(lambda x: get_device_reading_for_period(start_date, end_date, x.id), devices)
    total_kwh = sum(list(reading_collections))

    return total_kwh

def get_reading_stats(user_id, start_date, end_date):

    devices = Device.objects.filter(user__id = user_id)
    target = "total_kw"
    readings = []
    for device in devices:

        readings += [x[0] for x in  list(get_readings(device.id, start_date, end_date, target)) if x[0]>0]#UNWRAP TUPLES AND REMOVE INTEGER VALUES
    if len(readings) > 0:
        max_read = int(max(readings))
        min_read = int(min(readings))
        avg_read = int(sum(readings)/len(readings))
    else:
        min_read = max_read = avg_read = 0

    return max_read, min_read, avg_read

            ###########################################################################
            ####################                                    ###################
            ##################  JAVASCRIPT FILTER BY BRANCH AND TIME  #################
            ####################                                    ###################
            ###########################################################################

def js_get_readings(device_id, start_date, end_date, target):
    device = device.objects.get(id = device_id)
    readings = Reading.objects.filter(device = device, post_datetime__range = (start_date, end_date)).values_list(target)
 
    return readings

def js_get_device_reading_for_period(start_date, end_date, device_id):

    device = device.objects.get(id = device_id)
    readings = Reading.objects.filter(device = device, post_datetime__range = (start_date, end_date)).order_by("post_datetime").values_list('kwh_import')

    if len(readings) != 0:

        total_kwh_device  = readings[len(readings)-1][0] - readings[0][0]
    
    else:

        return 0

    return total_kwh_device

def js_total_energy(user_id, start_date, end_date, device_id = False):
    
    if device_id:
        devices = Device.objects.filter(id = device_id)
    else:
        devices = Device.objects.filter(user_id = user_id)

    reading_collections = map(lambda x: js_get_device_reading_for_period(start_date, end_date, x.id), devices)
    readings_as_list = list(reading_collections)

    total_kwh = sum(readings_as_list)
    return total_kwh

def js_get_reading_stats(user_id, start_date, end_date, device_id = False):

    target = "total_kw"
    readings = []

    if device_id:
        devices = Device.objects.filter(id = device_id)
    else:
        devices = Device.objects.filter(user_id = user_id)

    for device in devices:

        readings += [x[0] for x in  list(js_get_readings(device.id, start_date, end_date, target))if x[0] > 0]#UNWRAP TUPLES AND REMOVE INTEGER VALUES
    if len(readings) > 0:
        max_read = int(max(readings))
        min_read = int(min(readings))
        avg_read = int(sum(readings)/len(readings))
    else:
        min_read = max_read = avg_read = 0

    return max_read, min_read, avg_read

def format_date(date):###THIS FUNCTION CONVERTS DATE FROM DD-MM-YYY TO YYY-MM-DD

    month, day, year = date.split("-")
    formatted_date = f"{year.strip()}-{month.strip()}-{day.strip()}"
    datetime_object = datetime.strptime(formatted_date, '%Y-%m-%d')

    return datetime_object


            ############################################################################
            ####################                                     ###################
            ################## JAVASCRIPT FILTER BY PARAMETER AND TIME #################
            ####################                                     ###################
            ############################################################################


def js_get_readings_kw(device_id, start_date, end_date, target1, target2, target3):

    readings = Reading.objects.filter(device = device, post_datetime__range = (start_date, end_date)).values_list("post_datetime", target1, target2, target3)

    return readings


def get_js_power():

    time_now = datetime.now()
    start_date = "2019-07-01"
    end_date = "2019-07-02"

    data = js_get_readings_kw(1, start_date, end_date, "kw_l1", "kw_l2", "kw_l3" )

    data_as_df = pd.DataFrame(list(data), columns = ["time", "l1", "l2", "l3"],  index=None)

    data_as_df.index = data_as_df['time'] 
    data_as_df['hour']=data_as_df['time'].apply(lambda s:s.hour)

    hourly_data = data_as_df.groupby('hour').mean()
    
    read_qty = 8
    last_readings = hourly_data.tail(read_qty)
    last_readings_as_tuples = [tuple(reading) for reading in last_readings.values]
    

def get_energy_usage(devices):
        #TODAY READINGS STARTS TODAY AND ENDS TOMMORROW, WHILE YESTERDAY STARTS YESTERDAY AND ENDS TODAY.
        today_total = 0
        yesterday_total = 0

        today_start_date = datetime.now().date()
        today_end_date = today_start_date + timedelta(days = 1)
        
        yesterday_start_date = today_start_date  - timedelta(days = 1)
        yesterday_end_date = today_start_date

        for device in devices:
            
            today_readings = list(Reading.objects.filter(device = device, post_datetime__range = (today_start_date, today_end_date)).values_list("post_datetime", "kwh_import").order_by("post_time").values())

            yesterday_readings = list(Reading.objects.filter(device = device, post_datetime__range = (yesterday_start_date, yesterday_end_date)).values_list("post_datetime", "kwh_import").order_by("post_time").values())

            today_start = 0 if len(today_readings) < 1 else today_readings[0]["kwh_import"]
            today_end = 0 if len(today_readings) < 1 else today_readings[-1]["kwh_import"]

            yesterday_start = 0 if len(yesterday_readings) < 1 else yesterday_readings[0]["kwh_import"]
            yesterday_end = 0 if len(yesterday_readings) < 1 else yesterday_readings[-1]["kwh_import"]

            today_usage = today_end - today_start
            yesterday_usage = yesterday_end - yesterday_start

            today_total += today_usage
            yesterday_total += yesterday_usage
        
        return today_total, yesterday_total




# def get_energy_usage(device, start, end):
#     data = r.json()["data"]
# #     # print(data, "\n\n\n")
#     start = [i for i in data[-1]["data"] if i["description"] == "kWh import"][0]["value"]
#     end = [i for i in data[0]["data"] if i["description"] == "kWh import"][0]["value"]
#     usage = end - start
#     # print(start, "\n\n\n\n\n\n\n\n", end)
#     # print(usage)
    

# get_energy_usage(1,2,3)