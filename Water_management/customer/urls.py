from django.conf.urls import url
from .views import order, my_orders, view_order,order_confirmed,home

urlpatterns = [
    url(r'^home/$', home),
    url(r'^all-orders/$', my_orders),
    url(r'^order-confirmed/$', order_confirmed),
    url(r'^order/$', order),
    url(r'^order/(?P<order_id>[\w-]+)/$', view_order, name='order'),
]
