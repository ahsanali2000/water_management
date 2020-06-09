from django.db import models as md

class Person(md.Model):
    name = md.CharField(max_length=100, blank=False, null=False)
    phoneNo = md.CharField(max_length=11, blank=False, null=False)
    cnic = md.CharField(max_length=13, blank=False, null=False)
    username= md.CharField(max_length=50, unique=True)
    password= md.CharField(max_length=50)

class Customer(Person):
    noOfBottles = md.IntegerField(default=0)
    amountDue = md.IntegerField(default=0)
    approved = md.BooleanField(default=False)
    monthlyBill = md.IntegerField(default=0)
    user_type= md.IntegerField(default=3, editable=False)

class Employee(Person):
    salary = md.IntegerField(default=0)
    user_type= md.IntegerField(default=2, editable=False)

class Admin(md.Model):
    user_type= md.IntegerField(default=1, editable=False)
    username= md.CharField(max_length=50, unique=True)
    password= md.CharField(max_length=50)


class Address(md.Model):
    address = md.TextField(default="")
    person = md.ForeignKey(Person, on_delete=md.CASCADE)


class Vehicle(md.Model):
    registrationNo = md.CharField(max_length=15, blank=False, null=False)
    employee = md.ForeignKey(Employee, on_delete=md.SET_NULL, null=True)


class Order(md.Model):
    frequencyChoices = [(1, "One Time"), (2, "Recursive")]
    delivered = md.BooleanField(default=False)
    customer = md.ForeignKey(Customer, on_delete=md.CASCADE)
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