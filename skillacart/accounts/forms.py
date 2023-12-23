from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users


class CreateUserForm(UserCreationForm):
    """
    Form for user registration.
    Inherits from UserCreationForm provided by Django.
    """
    class Meta:
        model = Users
        fields = ['username', 'email', 'password1', 'password2', 'phone_number']