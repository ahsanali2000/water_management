from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^requests/$', account_requests),
    url(r'^all/$', list_view),
    url(r'^user/(?P<username>[ \w-]+)/$', details_view, name='details'),
    url(r'^allVehicles/$', all_vehicle, name='all_vehicle'),
    url(r'^newVehicle/$', add_vehicle),
    url(r'^allCities/$', all_cities),
    url(r'^newCity/$', add_city),
    url(r'^allAreas/(?P<city>[ \w-]+)$', all_areas, name='all_areas'),
    url(r'^newArea/$', add_area),
    url(r'^newEmployee/$', add_employee),
    url(r'^allEmployee/$', all_employee),
    url(r'^home/$', home, name='admin_home'),
    url(r'^editEmployee/(?P<username>[ \w-]+)$', edit_employee, name='edit_employee'),
    url(r'^profile/$', profile, name='adminProfile'),
    url(r'^editVehicle/(?P<regNo>[ \w-]+)$', edit_vehicle, name='edit_vehicle'),
    url(r'^selVehicle/(?P<page>[\w-]+)$', show_vehicle_for_schedule),
    url(r'^schedule/(?P<regNo>[ \w-]+)$', show_vehicle_schedule, name='show_schedule'),
    url(r'^updateSchedule/(?P<regNo>[ \w-]+)$', update_schedule, name='edit_schedule'),
    url(r'^orders/$', search_order, name='orders_admin'),
    url(r'^confirmOrder/(?P<id>[\w-]+)$', confirm_order, name='confirm_order_admin'),
    url(r'^selectVehicle/(?P<id>[\w-]+)$', select_vehicle_for_order, name='add_vehicle_to_order'),
    url(r'^newProduct/$', add_product, name='add_product'),
    url(r'^editProduct/(?P<code>[ \w-]+)$', edit_product, name='edit_product'),
    url(r'^allProduct/', all_products, name='all_product'),
    url(r'^records/$', show_records, name='records'),
    url(r'^approvePayment/(?P<id>[\w-]+)$', approve_payment, name="admin_approve_payment"),
]
