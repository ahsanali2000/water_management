from django.conf.urls import url
from .views import account_requests, list_view, details_view

urlpatterns = [
    url(r'^requests/$', account_requests),
    url(r'^all/$', list_view),
    url(r'^user/(?P<username>[\w-]+)/$', details_view, name='details')
]