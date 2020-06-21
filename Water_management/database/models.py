from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models as md
from django.urls import reverse
from django.utils.timezone import now

from accounts.models import CustomerManager, UserManager, EmployeeManager


class Person(AbstractBaseUser):
    username = md.CharField(max_length=30, default='', unique=True)
    email = md.CharField(verbose_name='email', max_length=100, default=' ', unique=True)
    password = md.CharField(max_length=100, )
    name = md.CharField(max_length=30, default=' ')
    PhoneNo = md.CharField(max_length=11, null=True, blank=True)
    cnic = md.CharField(max_length=13, null=True, blank=True)
    is_active = md.BooleanField(default=True)
    is_available = md.BooleanField(default=True)
    is_admin = md.BooleanField(default=False)
    is_staff = md.BooleanField(default=False)
    is_approved = md.BooleanField(default=False)
    is_customer = md.BooleanField(default=False)
    is_employee = md.BooleanField(default=False)
    created_at = md.DateTimeField(auto_now_add=True)
    updated_at = md.DateTimeField(auto_now=True)
    address = md.CharField(max_length=120, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']
    objects = UserManager()

    def get_url(self):
        return reverse('details', kwargs={'username': self.username})
    def get_url_customer(self):
        return reverse('customer_profile', kwargs={'username': self.username})
    def get_url_employee(self):
        return reverse('employee_profile', kwargs={'username': self.username})

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

    def __str__(self):
        return self.name


class Employee(Person):
    receivedAmount = md.IntegerField(default=0, null=False, blank=False)
    receivedBottle = md.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']
    objects = EmployeeManager()


class Customer(Person):
    NoOfBottles = md.IntegerField(default=0, null=True, blank=True)
    AmountDue = md.IntegerField(default=0, null=True, blank=True)
    MonthlyBill = md.IntegerField(default=0, null=True, blank=True)
    discounted_price = md.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']
    objects = CustomerManager()


class Vehicle(md.Model):
    registrationNo = md.CharField(max_length=15, blank=False, null=False, unique=True)
    employee = md.ForeignKey(Employee, on_delete=md.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.registrationNo


class Products(md.Model):
    name = md.CharField(max_length=80, null=False, blank=False)
    price = md.IntegerField(null=False, blank=False)
    code = md.CharField(max_length=2, primary_key=True)
    description = md.CharField(max_length=500, blank=True, null=True)


class Order(md.Model):
    frequencyChoices = [('1', "One Time"), ('2', "Recursive")]
    delivered = md.BooleanField(default=False)
    customer = md.ForeignKey(Customer, on_delete=md.CASCADE,
                             limit_choices_to={'is_customer': True}, related_name='%(class)s_is_customer')
    address = md.CharField(max_length=120, null=True, blank=True)
    desc = md.CharField(max_length=100)  # 'a1:0, a2:0' this is formate for system
    frequency = md.CharField(max_length=1, choices=frequencyChoices, default=frequencyChoices[0], blank=False,
                             null=False)
    ordered_at = md.DateTimeField(default=now)
    delivered_at = md.DateTimeField(null=True, blank=True, default=None)
    price = md.IntegerField(default=0)
    area = md.ForeignKey('Area', null=True, blank=True, on_delete=md.SET_NULL)
    confirmed = md.BooleanField(default=False)
    vehicle = md.ForeignKey(Vehicle, on_delete=md.SET_NULL, null=True)
    delivered_by = md.ForeignKey(Employee, on_delete=md.SET_NULL, null=True)

    def get_url(self):
        return reverse('order', kwargs={'order_id': self.id})
    def get_url_employee(self):
        return reverse('order_employee', kwargs={'order_id': self.id})
    def get_url_customer(self):
        return reverse('order_customer', kwargs={'order_id': self.id})


class City(md.Model):
    city = md.CharField(max_length=100, null=False, blank=False, unique=True)

    def __str__(self):
        return self.city


class Area(md.Model):
    city = md.ForeignKey(City, on_delete=md.CASCADE)
    name = md.CharField(max_length=100, null=False, blank=False)

    class Meta:
        unique_together = ('city', 'name',)

    def __str__(self):
        return "{}, {}".format(self.name, self.city)


class Schedule(md.Model):
    day_choices = [('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                   ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
    day = md.CharField(max_length=10, null=False, blank=False, choices=day_choices)
    areas = md.ManyToManyField(Area, null=True, blank=True)
    vehicle = md.ForeignKey(Vehicle, on_delete=md.CASCADE, null=True)
    order = md.IntegerField(null=False, default=0, blank=False)

    class Meta:
        unique_together = ('vehicle', 'day',)

    def __str__(self):
        return "{}, {}".format(self.day, self.vehicle)
