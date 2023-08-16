from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(
        label="First Name",
        required=True,
        max_length=32,
        error_messages={
            'required': 'Please enter your first name.',
            'invalid': 'Please enter your first name.'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name (Required)',
                'class': 'register-text21',
            }
        )
    )

    last_name = forms.CharField(
        label="Last Name",
        required=True,
        max_length=32, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name (Required)',
                'class' : 'register-text19',
            }
        )
    )

    email= forms.EmailField(
        label="Email",
        required=True,
        max_length=64, 
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email (Required)',
                'class' : 'register-text17',
            }
        )
    )

    password1 = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter your password',
                'class': 'register-text04',
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm your password',
                'class': 'register-text02',
            }
        )
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']