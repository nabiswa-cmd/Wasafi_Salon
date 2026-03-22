from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Appointment, CustomerProfile, Service
from django.utils import timezone
import datetime


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=15, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (e.g. 0712345678)'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            CustomerProfile.objects.create(
                user=user,
                phone=self.cleaned_data['phone']
            )
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AppointmentBookingForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': str(timezone.now().date() + datetime.timedelta(days=1))
        })
    )
    appointment_time = forms.TimeField(
        widget=forms.Select(attrs={'class': 'form-control'},
            choices=[
                ('09:00', '9:00 AM'), ('09:30', '9:30 AM'),
                ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
                ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
                ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
                ('13:00', '1:00 PM'), ('13:30', '1:30 PM'),
                ('14:00', '2:00 PM'), ('14:30', '2:30 PM'),
                ('15:00', '3:00 PM'), ('15:30', '3:30 PM'),
                ('16:00', '4:00 PM'), ('16:30', '4:30 PM'),
                ('17:00', '5:00 PM'),
            ]
        )
    )

    class Meta:
        model = Appointment
        fields = ['service', 'stylist', 'appointment_date', 'appointment_time', 'notes', 'payment_method']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'stylist': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3,
                                           'placeholder': 'Any special requests or notes?'}),
            'payment_method': forms.Select(
                attrs={'class': 'form-control'},
                choices=[('M-Pesa', 'M-Pesa'), ('Cash', 'Pay at Salon'), ('Card', 'Card')]
            ),
        }


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomerProfile
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
