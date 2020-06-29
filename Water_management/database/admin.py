from django.contrib import admin
from .models import Vehicle, Schedule, Products, City, Area, Order, Asset,CustomerAssets,Bottles

admin.site.register(Products)
admin.site.register(Order)
admin.site.register(Vehicle)
admin.site.register(Asset)
admin.site.register(CustomerAssets)
admin.site.register(Bottles)
