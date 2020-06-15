from django.contrib import admin
from .models import Vehicle,Schedule,Products,City,Area,Order

admin.site.register(Products)
admin.site.register(Order)