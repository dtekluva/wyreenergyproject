# import django
# from main.models import *
# from helpers.fetch_readings import run_migrations
# import time

# run_migrations()
# Datalog().populate()
# Device.populate_previous_scores

# def implicit():
#     from google.cloud import storage

#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()

#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)

# implicit()
from main.models import *
import json
from django.core.serializers.json import DjangoJSONEncoder


def load_score():

    device = Device.objects.get(device_id = device_id)
    user = User.objects.get(id = device.customer.user.id)
        # time_then = datetime.datetime.now()
        
        # device_id = request.POST.get("device", "None")
        
    branches = user.branch_set.all()
    response = []

    for branch in branches:

        devices = branch.device_set.all()

        # if not response.get(branch.name, False): 
                

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

    print(json.dumps({"response": "success", "data":{"base_line":response}}, sort_keys=True, indent=1, cls=DjangoJSONEncoder))