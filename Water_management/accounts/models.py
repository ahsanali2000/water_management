from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models as md

# Create your models here.
from django.urls import reverse


class CustomerManager(BaseUserManager):

    def create_user(self,
                        username=None,
                        email=None,
                        PhoneNo=None,
                        password=None,
                        cnic=None,
                        name=None,
                        NoOfBottles=0,
                        AmountDue=0,
                        MonthlyBill=0,

                        ):
        """
        Creates and saves a User with the given email and password.
        """
        if email is None:
            raise ValueError('Users must have an email address')
        if password is None:
            raise ValueError('Users must have a password')
        if  name is None:
            raise ValueError('Users must have a name')

        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.username=username
        user_obj.email=email
        user_obj.name=name
        user_obj.cnic=cnic
        user_obj.PhoneNo=PhoneNo
        user_obj.MonthlyBill=MonthlyBill
        user_obj.NoOfBottles=NoOfBottles
        user_obj.AmountDue=AmountDue
        user_obj.is_customer=True
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self,email, username, password,name,):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            name=name,
            email=email,
            username=username,
            password=password
        )

        user.is_staff=True
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserManager(BaseUserManager):
    def create_user(self,
                        username=None,
                        email=None,
                        PhoneNo=None,
                        password=None,
                        cnic=None,
                        name=None,
                        ):
        """
        Creates and saves a User with the given email and password.
        """
        if email is None:
            raise ValueError('Users must have an email address')
        if password is None:
            raise ValueError('Users must have a password')
        if name is None:
            raise ValueError('Users must have a name')
        user_obj = self.model(
            email=self.normalize_email(email),
        )
        user_obj.username = username
        user_obj.email = email
        user_obj.name = name
        user_obj.cnic = cnic
        user_obj.PhoneNo = PhoneNo
        user_obj.set_password(password)
        user_obj.save(using=self._db)
        return user_obj

    def create_employee(self,cnic=None, PhoneNo=None,name=None, password=None,username=None,email=None):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username=username,
            name=name,
            email=email,
            PhoneNo=PhoneNo,
        )

        user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, username, password,name,):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            name=name,
            email=email,
            username=username,
            password=password
        )

        user.is_staff=True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    username = md.CharField(max_length=30, default='',unique=True)
    email = md.CharField(verbose_name='email', max_length=100,default=' ', unique=True)
    password = md.CharField(max_length=100, )
    name = md.CharField(max_length=30,default=' ')
    PhoneNo = md.CharField(max_length=11, null=True, blank=True)
    cnic = md.CharField(max_length=13,null=True, blank=True)
    is_active = md.BooleanField(default=True)
    is_admin = md.BooleanField(default=False)
    is_staff = md.BooleanField(default=False)
    is_approved = md.BooleanField(default=False)
    is_customer=md.BooleanField(default=False)
    is_employee=md.BooleanField(default=False)
    created_at = md.DateTimeField(auto_now_add=True)
    updated_at = md.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','email']
    objects = CustomerManager()


    def get_url(self):
        return reverse('details', kwargs={'username':self.username})
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

class Customer(Person):
    NoOfBottles = md.IntegerField(default=0, null=True, blank=True)
    AmountDue = md.IntegerField(default=0, null=True, blank=True)
    MonthlyBill = md.IntegerField(default=0, null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']
    objects = CustomerManager()
    def get_url(self):
        return reverse('details', kwargs={'username':self.username})