from django.core.management.base import BaseCommand
from main.models import *


class Command(BaseCommand):
    help = 'alerts customers of load inbalance'

    def handle(self, *args, **kwargs):
        try:

            users = User.objects.all()

            for user in users:
                                
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

            self.stdout.write("Update Readings Successfull")

        except:
            
            self.stdout.write("Update Readings Failed")              