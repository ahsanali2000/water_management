from django.contrib import admin
from .models import Person,Customer

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin





admin.site.register(Person)
admin.site.register(Customer)