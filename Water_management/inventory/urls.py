from django.conf.urls import url
from .views import all_assets

urlpatterns = [
    url(r'^all/$', all_assets, name='all_assets'),

]
