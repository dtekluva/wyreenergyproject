"""resolute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('power/', views.power, name='power'),
    path('last_read/', views.last_read, name='last_read'),
    path('get_last_read/', views.get_last_read, name='get_last_read'),
    path('score_card/', views.score_card, name='score_card'),
    path('voltage/', views.voltage, name='voltage'),
    path('current/', views.current, name='current'),
    path('readings/', views.readings, name='readings'),
    path('energy_readings/', views.energy_readings, name='energy_readings'),
    path('get_energy_readings/', views.get_energy_readings, name='get_energy_readings'),
    path('get_line_readings/', views.get_line_readings, name='get_line_readings'),
    path('max_demand/', views.max_demand, name='max_demand'),
    path('fetch_vals_period/', views.fetch_vals_period, name='fetch_vals_period'),
    path('fetch_device_vals/', views.fetch_vals_period_per_device, name='fetch_vals_period_per_device'),
    path('load_datalogs/', views.load_datalogs, name='load_datalogs'),
    path('load_readings/', views.load_readings, name='load_readings'),
    path('get_yesterday_today_usage/', views.get_yesterday_today_usage, name='get_yesterday_today_usage'),
    path('get_line_readings_log/', views.get_line_readings_log, name='get_line_readings_log'),
    path('get_capacity_factors/', views.get_capacity_factors, name='get_capacity_factors'),
    path('messaging/', views.messaging, name='messaging'),
    path('fetch_messages/', views.fetch_messages, name='fetch_messages'),
    path('check_new_message/', views.check_new_message, name='check_new_message'),
    path('send_message/', views.send_message, name='send_message'),
    path('simple_upload/', views.simple_upload, name='simple_upload'),
    path('upload_cdd/', views.upload_cdd, name='upload_cdd'),
    path('all_customers/', views.all_customers, name='all_customers'),
    path('view_customer/<int:id>', views.view_customer, name='view_customer'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('update_details/', views.update_details, name='update_details'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('update_branch/', views.update_branch, name='update_branch'),
    path('update_device/', views.update_device, name='update_device'),
    path('create_branch/', views.create_branch, name='create_branch'),
    path('create_device/', views.create_device, name='create_device'),
    path('update_historic_scores/', views.update_historic_scores, name='update_historic_scores'),
    path('get_total_energy/', views.get_total_energy, name='get_total_energy'),
    path('get_stats/', views.get_stats, name='get_stats'),
    # path('detail_view', views.detail_view, name='detail_view'),
    # path('locationpost', views.locationpost, name='locationpost'),
    # path('incidents', views.incidents, name='incidents'),
    # path('table', views.table, name='table'),
    # path('logs', views.logs, name='logs'),
    # # path('track', views.track, name='track')
    # path('check/<slug:slug>/', views.check, name='check'),
    # path('collection_check/<int:id>/', views.collection_check, name='collection_check'),
    # path('track/<slug:slug>/', views.track, name='track'),
    # path('trail/<slug:slug>/', views.trail, name='trail'),
    # path('mapping/<slug:slug>/', views.mapping, name='mapping'),
    # path('get_lat_lng/<slug:id>', views.get_lat_lng, name='get_lat_lng'),# FOR PROFILE REALTIME MAP
    # path('get_latlng/<slug:username>', views.get_latlng, name='get_latlng'),
    # path('get_latlng_incident/<slug:username>/<slug:incident>/', views.get_latlng_incident, name='get_latlng_incident'),
    # path('post_latlng', views.post_latlng, name='post_latlng'),
    # path('check_panic', views.check_panic, name='check_panic'),
    # path('create_panic', views.create_panic, name='create_panic'),
    # path('resolve_panic_mobile', views.resolve_panic_mobile, name='resolve_panic_mobile'),
    # path('resolve_panic', views.resolve_panic, name='resolve_panic'),
    # path('recurring_gps_post', views.recurring_gps_post, name='recurring_gps_post'),
    # path('farmers', views.farmers, name='farmers'),
    # path('herdsmen', views.herdsmen, name='herdsmen'),
    # path('get_client_data', views.get_client_data, name='get_client_data'),
    # path('profile_page/<int:target_id>/<slug:is_farmer>', views.profile_page, name='profile_page')
    
    # path('test', views.test, name='test'),
]
