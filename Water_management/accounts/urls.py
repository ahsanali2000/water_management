
from django.conf.urls import url
from .views import login_user, logout_user, register_user

urlpatterns = [
    url(r'^login/$', login_user, name='LogIn'),
    url(r'^logout/$', logout_user),
    url(r'^register/$', register_user),

]
