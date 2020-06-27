from django.contrib import admin
from .models import Vehicle, Schedule, Products, City, Area, Order, Asset, Corporate

admin.site.register(Corporate)
admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Asset)
