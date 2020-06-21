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
            'address'
        ]

    def clean_confirm_pass(self):
        print('im running')
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_pass")
        print(password2)
        print(self.cleaned_data)
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
