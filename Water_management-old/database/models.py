from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models as md



class Address(md.Model):
    address = md.TextField(default="")
    person = md.ForeignKey(settings.AUTH_USER_MODEL, on_delete=md.CASCADE)


class Vehicle(md.Model):
    registrationNo = md.CharField(max_length=15, blank=False, null=False)
    employee = md.ForeignKey(settings.AUTH_USER_MODEL, on_delete=md.SET_NULL, null=True)


class Order(md.Model):
    frequencyChoices = [(1, "One Time"), (2, "Recursive")]
    delivered = md.BooleanField(default=False)
    customer = md.ForeignKey(settings.AUTH_USER_MODEL, on_delete=md.CASCADE)#remember there is need of customer id but its person
    frequecy = md.CharField(max_length=10, choices=frequencyChoices, default=frequencyChoices[0], blank=False,
                            null=False)
    date = md.DateTimeField()
    desc = md.CharField(max_length=100)#'a1:0, a2:0' this is formate for system

class City(md.Model):
    city = md.CharField(max_length=100, null=False, blank=False)


class Area(md.Model):
    city = md.ForeignKey(City, on_delete=md.CASCADE)
    area = md.CharField(max_length=100, null=False, blank=False)
    addresses = md.ManyToManyField(Address)

class Schedule(md.Model):
    day = md.CharField(max_length=10, null=False, blank=False)
    areas = md.ManyToManyField(Area)

class Products(md.Model):
    name = md.CharField(max_length=80, null=False, blank=False)
    prince = md.IntegerField(null=False, blank=False)
    code = md.CharField(max_length=2)

    # from django.contrib.auth.models import User
    # from django.db import models as md
    #
    #
    #
    # class Person(md.Model):
    #     user = md.OneToOneField(User,on_delete=md.CASCADE)
    #     phoneNo = md.CharField(max_length=11, blank=False, null=False)
    #     cnic = md.CharField(max_length=13, blank=False, null=False)
    #     is_active = md.BooleanField(default=True)
    #     is_admin = md.BooleanField(default=False)
    #     is_customer=md.BooleanField(default=False)
    #     is_employee=md.BooleanField(default=False)

