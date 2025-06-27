from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import Customer


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    age = forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class': 'form-input'}))
    tel_number = forms.IntegerField(label='Telephone number', widget=forms.TelInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Customer
        fields = ('username', 'email', 'age', 'tel_number', 'password1', 'password2')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'class': 'form-input'}),
            'tel_number': forms.TelInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('username', 'email', 'age', 'tel_number')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'age': forms.NumberInput(attrs={'class': 'form-input'}),
            'tel_number': forms.TelInput(attrs={'class': 'form-input'}),
        }