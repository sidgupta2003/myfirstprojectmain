from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product, ROLE_CHOICES, User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        if user and user.role == 'admin':
            self.fields['role'].choices = [('user', 'User')]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']