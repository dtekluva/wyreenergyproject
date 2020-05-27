import requests
from requests.auth import HTTPBasicAuth
import json


req = requests.get('http://expertpowerplus.com:8080/api/Login?userName=ppl&pass=Wyre2017')

auth_key_name = (list(req.cookies)[0]).name #get name of cookie unit used to be (.ASPXAUTH) changed to (form_p)
auth_key_value = dict(req.cookies).get(auth_key_name) #get actual cookie unit

cookie = {auth_key_name: auth_key_value}

# r = requests.get('http://expertpowerplus.com:8080/api/basic/133813/LastReading', cookies=cookie)
r = requests.get('http://www.expertpowerplus.com:8080/api/basic/133813/Datalogs?startDate=2019-10-01&endDate=2019-10-20&datalogNum=1', cookies=cookie)


x = (r.content)

data = json.loads(x)
readings = (data['data'][0]['data'])

for value in readings:
    # print(value["description"], end= '*')


readings = (data['data'][0]['data'])

for value in readings:
    # print((value["description"]).center(40), str(value["value"]).center(13), str(value["units"]).center(13))
    




# # print(data.get("data"))


# text = 'Voltage L1/L12*Voltage L2/L23*Voltage L3/L31*Current L1*Current L2*Current L3*kW L1*kW L2*kW L3*kvar L1*kvar L2*kvar L3*kVA L1*kVA L2*kVA L3*Power factor L1*Power factor L2*Power factor L3*Total kW*Total kvar*Total kVA*Total PF*Avg Frequency*Neutral current*Volt THD L1/L12*Volt THD L2/L23*Volt THD L3/L31*Current THD L1*Current THD L2*Current THD L3*Current TDD L1*Current TDD L2*Current TDD L3*kWh import*kWh export*kvarh import*kVAh total*Max Amp. Demand L1*Max Amp. Demand L2*Max Amp. Demand L3*Max. sliding window kW Demand*Accum. kW Demand*Max. sliding window kVA Demand*Present sliding window kW Demand*Present sliding window kVA Demand*Accum. kVA Demand*PF (import) at maximum kVA sliding window Demand'.replace(' ','_').replace('/','_')
# parameters = text.split('*')
# model = ' = models.FloatField(null=True, blank=True, default=None)'

# for value in parameters:
#     # # print(value + model)



# well_formatted_models = """    Voltage_L1_L12  = models.FloatField(null=True, blank=True, default=None)
#     Voltage_L2_L23  = models.FloatField(null=True, blank=True, default=None)
#     Voltage_L3_L31  = models.FloatField(null=True, blank=True, default=None)
#     Current_L1      = models.FloatField(null=True, blank=True, default=None)
#     Current_L2      = models.FloatField(null=True, blank=True, default=None)
#     Current_L3      = models.FloatField(null=True, blank=True, default=None)
#     kW_L1   = models.FloatField(null=True, blank=True, default=None)
#     kW_L2   = models.FloatField(null=True, blank=True, default=None)
#     kW_L3   = models.FloatField(null=True, blank=True, default=None)
#     kvar_L1 = models.FloatField(null=True, blank=True, default=None)
#     kvar_L2 = models.FloatField(null=True, blank=True, default=None)
#     kvar_L3 = models.FloatField(null=True, blank=True, default=None)
#     kVA_L1  = models.FloatField(null=True, blank=True, default=None)
#     kVA_L2  = models.FloatField(null=True, blank=True, default=None)
#     kVA_L3  = models.FloatField(null=True, blank=True, default=None)
#     Power_factor_L1  = models.FloatField(null=True, blank=True, default=None)
#     Power_factor_L2  = models.FloatField(null=True, blank=True, default=None)
#     Power_factor_L3  = models.FloatField(null=True, blank=True, default=None)
#     Total_kW    = models.FloatField(null=True, blank=True, default=None)
#     Total_kvar  = models.FloatField(null=True, blank=True, default=None)
#     Total_kVA   = models.FloatField(null=True, blank=True, default=None)
#     Total_PF    = models.FloatField(null=True, blank=True, default=None)
#     Avg_Frequency   = models.FloatField(null=True, blank=True, default=None)
#     Neutral_current = models.FloatField(null=True, blank=True, default=None)
#     Volt_THD_L1_L12 = models.FloatField(null=True, blank=True, default=None)
#     Volt_THD_L2_L23 = models.FloatField(null=True, blank=True, default=None)
#     Volt_THD_L3_L31 = models.FloatField(null=True, blank=True, default=None)
#     Current_THD_L1  = models.FloatField(null=True, blank=True, default=None)
#     Current_THD_L2  = models.FloatField(null=True, blank=True, default=None)
#     Current_THD_L3  = models.FloatField(null=True, blank=True, default=None)
#     Current_TDD_L1  = models.FloatField(null=True, blank=True, default=None)
#     Current_TDD_L2  = models.FloatField(null=True, blank=True, default=None)
#     Current_TDD_L3  = models.FloatField(null=True, blank=True, default=None)
#     kWh_import      = models.FloatField(null=True, blank=True, default=None)
#     kWh_export      = models.FloatField(null=True, blank=True, default=None)
#     kvarh_import    = models.FloatField(null=True, blank=True, default=None)
#     kVAh_total      = models.FloatField(null=True, blank=True, default=None)
#     Max_Amp._Demand_L1 = models.FloatField(null=True, blank=True, default=None)
#     Max_Amp._Demand_L2 = models.FloatField(null=True, blank=True, default=None)
#     Max_Amp._Demand_L3 = models.FloatField(null=True, blank=True, default=None)
#     Max._sliding_window_kW_Demand   = models.FloatField(null=True, blank=True, default=None)
#     Accum._kW_Demand    = models.FloatField(null=True, blank=True, default=None)
#     Max._sliding_window_kVA_Demand      = models.FloatField(null=True, blank=True, default=None)
#     Present_sliding_window_kW_Demand    = models.FloatField(null=True, blank=True, default=None)
#     Present_sliding_window_kVA_Demand   = models.FloatField(null=True, blank=True, default=None)
#     Accum_kVA_Demand   = models.FloatField(null=True, blank=True, default=None)
#     PF_import_at_maximum_kVA_sliding_window_Demand = models.FloatField(null=True, blank=True, default=None)"""    


# for attribute in well_formatted_models.split("\n"):
#     splitted_attribute = attribute.split("= ") 
#     lowered_attribute_name = splitted_attribute[0].lower()
#     # # print(lowered_attribute_name + "= " + splitted_attribute[1], "/n")

