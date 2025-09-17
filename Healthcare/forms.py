from django import forms
from .models import *


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'age', 'phone', 'gender', 'specialist', 'appointment_date', 'time_slot']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient full name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter patient age'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'specialist': forms.Select(attrs={'class': 'form-select'}),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Name',
            'age': 'Age',
            'phone': 'Phone Number',
            'gender': 'Gender',
            'specialist': 'Select Consultant',
            'appointment_date': 'Appointment Date',
            'time_slot': 'Preferred Time Slot',
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'})
    )
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'})
    )
    mobile = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number'})
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'mobile', 'password']

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        mobile = cleaned_data.get('mobile')

        # Check password match
        if password != confirm:
            errors['password'] = "Passwords do not match"

        # Check mobile digits only
        if not mobile.isdigit():
            errors['mobile'] = "Mobile number must contain digits only"

        # Check mobile uniqueness
        if CustomUser.objects.filter(mobile=mobile).exists():
            errors['mobile'] = "Mobile number already exists"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data




class UserLoginForm(forms.Form):
    mobile = forms.CharField(
        label="Mobile Number",
        max_length=15,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})
    )


from django import forms
from .models import StaffUser

class StaffRegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm password'})
    )
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your name'})
    )
    mobile = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number'})
    )

    class Meta:
        model = StaffUser
        fields = ['name', 'mobile', 'password']

    def clean(self):
        cleaned_data = super().clean()
        errors = {}

        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        mobile = cleaned_data.get('mobile')

        if password != confirm:
            errors['password'] = "Passwords do not match"

        if not mobile.isdigit():
            errors['mobile'] = "Mobile number must contain digits only"

        if StaffUser.objects.filter(mobile=mobile).exists():
            errors['mobile'] = "Mobile number already exists"

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data




class StaffLoginForm(forms.Form):
    mobile = forms.CharField(
        label="Mobile Number",
        max_length=15,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter password'})
    )