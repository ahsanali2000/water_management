
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import login_user,logout_user,register_user,account_requests,list_view,details_view


urlpatterns = [
    url(r'^login/$',login_user),
    url(r'^logout/$',logout_user),
    url(r'^register/$', register_user),
    url(r'^requests/$', account_requests),
    url(r'^all/$', list_view),
    url(r'^user/(?P<username>[\w-]+)/$',details_view,name='details')
]