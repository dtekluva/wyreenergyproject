from main.models import Reading, Device
import requests
from requests.auth import HTTPBasicAuth
import json, datetime, pytz
from dateutil.parser import parse

lagos=pytz.timezone('Africa/Lagos')

username = "ppl"
password = "Wyre2017"
device_ids = ["128162","125639","128166", "133813"]

last_reading = ""

def authenticate(username, password):#LOGIN TO EXPERT POWER PLUS

    req = requests.get(f'http://expertpowerplus.com:8080/api/Login?userName={username}&pass={password}')
    # # print(req.cookies)
    auth_key_name = (list(req.cookies)[0]).name #get name of cookie unit used to be (.ASPXAUTH) changed to (form_p)
    auth_key_value = dict(req.cookies).get(auth_key_name) #get actual cookie unit

    cookie = {auth_key_name: auth_key_value}

    return cookie

def make_request(cookie, device_id, start_date, end_date):
    
    request = requests.get(f'http://expertpowerplus.com:8080/api/Basic?startDate={start_date}&endDate={end_date}&deviceId={device_id}', cookies=cookie)

    response = request.content
    data = json.loads(response)
    readings = data['data']
#     # print(data)
    return readings


def populate_db(readings, device_code, last_reading):

    device = Device.objects.get(device_id = device_code)
    first_run = True
#     print(readings)

    for record in reversed(readings):
        # date = record['recordTime'][:10]
        # time = record['recordTime'][11:]
        # _datetime = (record['recordTime']).replace('T'," ")
        time_obj = lagos.localize(parse(record['recordTime']))
        # print(record)

        if first_run : print("-----RUNNING MIGRATION-----"); first_run = False
        # print(lagos.localize(parse(record['recordTime'])) > last_reading)

        if lagos.localize(parse(record['recordTime'])) > last_reading:
                reading = reshape_data_to_dict(record["data"])
                # print(readings)
                
                Reading.objects.create(customer = device.customer, post_date = time_obj, post_time = time_obj, 
                        post_datetime = time_obj, 
                        device_id   =  device.id,
                        user_id = device.user_id,
                        voltage_l1_l12 =  reading.get("voltage_l1_l12", 0),
                        voltage_l2_l23 = reading.get("voltage_l2_l23", 0),
                        voltage_l3_l31 = reading.get("voltage_l3_l31", 0),
                        current_l1     = reading.get("current_l1", 0),
                        current_l2     = reading.get("current_l2", 0),
                        current_l3     = reading.get("current_l3", 0),
                        kw_l1   = reading.get("kw_l1", 0),
                        kw_l2   = reading.get("kw_l2", 0),
                        kw_l3   = reading.get("kw_l3", 0),
                        kvar_l1 = reading.get("kvar_l1", 0),
                        kvar_l2 = reading.get("kvar_l2", 0),
                        kvar_l3 = reading.get("kvar_l3", 0),
                        kva_l1  = reading.get("kva_l1", 0),
                        kva_l2  = reading.get("kva_l2", 0),
                        kva_l3  = reading.get("kva_l3", 0), 
                        power_factor_l1  = reading.get("power_factor_l1", 0),
                        power_factor_l2  = reading.get("power_factor_l2", 0),
                        power_factor_l3  = reading.get("power_factor_l3", 0),
                        total_kw    = reading.get("total_kw", 0),
                        total_kvar  = reading.get("total_kvar", 0),
                        total_kva   = reading.get("total_kva", 0),
                        total_pf    = reading.get("total_pf", 0),
                        avg_frequency   = reading.get("avg_frequency", 0),
                        neutral_current = reading.get("neutral_current", 0),
                        volt_thd_l1_l12 = reading.get("volt_thd_l1_l12", 0),
                        volt_thd_l2_l23 = reading.get("volt_thd_l2_l23", 0), 
                        volt_thd_l3_l31 = reading.get("volt_thd_l3_l31", 0), 
                        current_thd_l1 = reading.get("current_thd_l1", 0), 
                        current_thd_l2 = reading.get("current_thd_l2", 0),
                        current_thd_l3 = reading.get("current_thd_l3", 0),
                        current_tdd_l1 = reading.get("current_tdd_l1", 0),
                        current_tdd_l2 = reading.get("current_tdd_l2", 0),
                        current_tdd_l3 = reading.get("current_tdd_l3", 0),
                        kwh_import      = reading.get("kwh_import", 0),
                        kwh_export      = reading.get("kwh_export", 0),
                        kvah_total      = reading.get("kvah_total", 0),
                        kvarh_import      = reading.get("kvarh_import", 0),
                        max_amp_demand_l1 = reading.get("max_amp_demand_l1", 0),
                        max_amp_demand_l2 = reading.get("max_amp_demand_l2", 0),
                        max_amp_demand_l3 = reading.get("max_amp_demand_l3", 0),
                        max_sliding_window_kw_demand  = reading.get("max_sliding_window_kw_demand", 0),
                        accum_kw_demand = reading.get("accum_kw_demand", 0),
                        accum_kva_demand = reading.get("accum_kva_demand", 0),
                        max_sliding_window_kva_demand = reading.get("max_sliding_window_kva_demand", 0),
                        present_sliding_window_kw_demand  = reading.get("present_sliding_window_kw_demand", 0),
                        present_sliding_window_kva_demand = reading.get("present_sliding_window_kva_demand", 0),
                        pf_import_at_maximum_kva_sliding_window_demand = reading.get("pf_import_at_maximum_kva_sliding_window_demand", 0)
                )
                # print(0)
        
    else: 
        print("------Done populating------")

def update_user_readings(user_id):
        last_update = (Reading.objects.filter(user_id = user_id).order_by("-id")[0]).post_datetime
        
def reshape_data_to_dict(readings):
        i = 0
        # # print(readings)

        parameters = {}
        for value in readings:
                description = (value["description"])\
                                .replace('.','')\
                                .replace(' ','_')\
                                .replace('/','_')\
                                .replace('(','')\
                                .replace(')','').lower()
                # # print(str(i).center(2), description.center(35), str(value["value"]).center(12), str(value["units"]).center(13))
                parameters[description] = value["value"]
                i += 1
        return parameters

def run_migrations():
        cookies = authenticate(username,password)
        device_ids = Device.objects.all()
        
        for device in device_ids:
                print(device.device_id)
                
                # target_device = Device.objects.get(device_id = device_id)
                last_reading = Reading.objects.filter(device = device).latest('post_datetime').post_datetime #GET LAST READING FOR PARTICULAR DEVICE
                tommorow = datetime.datetime.now() + datetime.timedelta(days = 1)#GET TODAYS DATE AND ADD ONE DAY

                start_date = f"{last_reading.year}-{last_reading.month}-{last_reading.day}" #"2019-08-18"
                end_date = f"{tommorow.year}-{tommorow.month}-{tommorow.day}"

                readings = make_request(cookies, device.device_id, start_date, end_date)
                # # print(readings)
                populate_db(readings, device.device_id, last_reading)