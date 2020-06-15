from django import forms
from database.models import Person, City, Area, Vehicle, Schedule, Customer


class EmployeeCreateForm(forms.ModelForm):
    confirmPassword = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Person
        fields = ['name', 'username', 'email', 'cnic', 'password', 'confirmPassword', 'PhoneNo']
        labels = {'name': 'Name', 'username': 'Username', 'email': 'Email', 'cnic': 'CNIC', 'password': 'Password',
                  'confirmPassword': "Re-enter Password", 'PhoneNo': "Phone number"}
        widgets = {
            'password': forms.PasswordInput
        }

    def clean_confirmPassword(self):
        password = self.cleaned_data.get('password')
        confirmPassword = self.cleaned_data.get('confirmPassword')
        if password == confirmPassword:
            return confirmPassword
        return ValueError("Passwords Do not Match")

    def clean_is_employee(self):
        return True

    def save(self, commit=True):
        employee = super().save(commit=False)
        employee.set_password(self.cleaned_data['password'])
        employee.save()
        return employee


class CityCreateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city']
        labels = {'city': "City"}


class AreaCreateForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['city', 'area']
        labels = {"city": "City", "area": "Area"}


class VehicleCreateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registrationNo', 'employee']
        labels = {"registrationNo": "Registration Number", "employee": "Employee"}


class ScheduleCreateForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'areas']
        labels = {'day': "Day", 'areas': "Areas"}
        widgets = {
            'areas': forms.SelectMultiple(
                attrs={
                    'class': 'mdb-select md-form colorful-select dropdown-primary',
                    'multiple searchable': 'Search here..'
                }
            ),
        }

    def clean_day(self):
        day = self.cleaned_data['day']
        week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if day in week:
            return day
        return ValueError("Day is not in week")


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'cnic', 'PhoneNo', 'MonthlyBill', 'NoOfBottles',
                  'AmountDue']
        labels = {'name': 'Name', 'email': 'Email', 'cinc': 'CNIC', 'PhoneNo': 'Phone No',
                  'MonthlyBill': 'Monthly Bill', 'AmountDue': 'Amount Due'}