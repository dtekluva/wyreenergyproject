import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from dateutil import parser
import numpy as np


def make_remote_request(device_id, start_date = "2019-08-15", end_date = "2019-08-16", url = 'logs'):

    req = requests.get('http://expertpowerplus.com:8080/api/Login?userName=ppl&pass=Wyre2017')

    auth_key_name = (list(req.cookies)[0]).name #get name of cookie unit used to be (.ASPXAUTH) chnaged to (form_p)
    auth_key_value = dict(req.cookies).get(auth_key_name) #get actual cookie unit
    cookie = {auth_key_name: auth_key_value}
    # device_id = "128166" #2019-04-15

    url_data_logs = f'http://www.expertpowerplus.com:8080/api/basic/{device_id}/Datalogs?startDate={start_date}&endDate={end_date}&datalogNum=1'

    url_last_read = f'http://expertpowerplus.com:8080/api/basic/{device_id}/LastReading'

    url = url_data_logs if url == "logs" else url_last_read

    r = requests.get(url, cookies=cookie)
    return r.json()

