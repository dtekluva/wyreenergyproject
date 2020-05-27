from django.contrib import admin
from main.models import *
# Register your models here.

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'customer' )

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'phone' )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('customer', 'branch', 'phone' )

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_id', 'customer', 'location', "branch" )

class ReadingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'device', 'post_time', 'post_date' )

class DatalogAdmin(admin.ModelAdmin):
    list_display = ('device', 'post_time', 'post_date' )

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', )

class Degree_DayAdmin(admin.ModelAdmin):
    list_display = ('date', 'value')

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('date', 'device')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id',)



admin.site.register(Branch, BranchAdmin)
admin.site.register(Document,DocumentAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Reading, ReadingAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Degree_Day, Degree_DayAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Datalog, DatalogAdmin)