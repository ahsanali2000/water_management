from django.db import models as md


class Customer(md.Model):
    name = md.CharField(max_length=100, blank=False, null=False)
    phoneNo = md.CharField(max_length=11, blank=False, null=False)
    addresses = md.ManyToManyField("Address")
    cnic = md.CharField(max_length=13, blank=False, null=False)
    noOfBottles = md.IntegerField(default=0)
    amountDue = md.IntegerField(default=0)
    approved = md.BooleanField(default=False)
    monthlyBill = md.IntegerField(default=0)


class Address(md.Model):
    address = md.TextField(default="")


class Employee(md.Model):
    name = md.CharField(max_length=100, blank=False, null=False)
    phoneNo = md.CharField(max_length=11, blank=False, null=False)
    cnic = md.CharField(max_length=13, null=False, blank=False)


class Vehicle(md.Model):
    registrationNo = md.CharField(max_length=15, blank=False, null=False)
    employee = md.ForeignKey(Employee, on_delete=md.SET_NULL, null=True)


class Order(md.Model):
    frequencyChoices = [(1, "One Time"), (2, "Recursive")]
    customer = md.ForeignKey(Customer, on_delete=md.CASCADE)
    frequecy = md.CharField(max_length=10, choices=frequencyChoices, default=frequencyChoices[0], blank=False,
                            null=False)
    date = md.DateTimeField()


class City(md.Model):
    city = md.CharField(max_length=100, null=False, blank=False)


class Area(md.Model):
    city = md.ForeignKey(City, on_delete=md.CASCADE)
    area = md.CharField(max_length=100, null=False, blank=False)
    addresses = md.ManyToManyField(Address)

class Schedule(md.Model):
    day = md.CharField(max_length=10, null=False, blank=False)
    areas = md.ManyToManyField(Area)