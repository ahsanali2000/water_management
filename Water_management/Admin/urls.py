from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^requests/$', account_requests),
    url(r'^all/$', list_view),
    url(r'^user/(?P<username>[\w-]+)/$', details_view, name='details'),
    url(r'allVehicles/', all_vehicle),
    url(r'newVehicle/', add_vehicle),
    url(r'allCities/', all_cities),
    url(r'newCity/', add_city),
    url(r'allAreas/<str:city>', all_areas),
    url(r'newArea/', add_area),
    url(r'allOrder/', all_orders),
    url(r'newEmployee/', add_employee),
    url(r'allEmployee/', all_employee),
    url(r'^home/$', home),
]