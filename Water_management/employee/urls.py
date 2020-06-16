from django.conf.urls import url
from .views import home,confirmed_not_delivered_orders,not_confirmed,delivered_orders

urlpatterns = [
    url(r'^home/$', home),
    url(r'^confirmed_not_delivered_orders/$', confirmed_not_delivered_orders),
    url(r'^not_confirmed/$', not_confirmed),
    url(r'^delivered_orders/$', delivered_orders),
]