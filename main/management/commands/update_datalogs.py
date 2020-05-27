from django.core.management.base import BaseCommand
from main.models import *
from main.helpers.fetch_readings import run_migrations



class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        try:

            for i in range(5):

                Datalog().populate()
                 
            self.stdout.write("Update Datalogs Successfull")

        except:
            
            self.stdout.write("Update Datalogs Failed")              
      


# def update_historic_scores(request):

#         devices = Device.objects.all()                        

#         for device in devices:
#                 device.populate_previous_scores()
