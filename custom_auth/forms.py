from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product, ROLE_CHOICES

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email field
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']