from django.core.management.base import BaseCommand
from main.models import *
from main.helpers.fetch_readings import run_migrations




# def update_historic_scores(request):

#         devices = Device.objects.all()                        

#         for device in devices:
#  
class Command(BaseCommand):
    help = 'alerts customers of load inbalance'

    def handle(self, *args, **kwargs):
        try:

            devices = Device.objects.all()
                
            for device in devices:

                device.check_load_balance()

            self.stdout.write("Update Readings Successfull")

        except:
            
            self.stdout.write("Update Readings Failed")              