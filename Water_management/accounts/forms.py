from django import forms

from database.models import Customer


class CustomerRegisterForm(forms.ModelForm):
    confirm_pass = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Customer
        labels = {
            "cnic": "CNIC",
            'email': 'Email Address',
            'PhoneNo': 'Phone Number',
            'AverageWeekly' : 'Your estimated average consumptions of 19 Litre bottles per week'
        }
        widgets = {
            'password': forms.PasswordInput,
        }
        fields = [
            'name',
            'username',
            'email',
            'cnic',
            'is_customer',
            'password',
            'PhoneNo',
            'address',
            'AverageWeekly',
        ]

    def clean_confirm_pass(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_pass")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_is_customer(self):
        return True

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
