from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product, ROLE_CHOICES, User, ROLE_CHOICESS
from django import forms

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update({'placeholder': self.fields[field_name].label})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
    # email = forms.EmailField(required=True)  
    # role = forms.ChoiceField(choices=ROLE_CHOICESS, required=True)

    # class Meta:
    #     model = CustomUser
    #     fields = ['username', 'email', 'password1', 'password2', 'role']
    #     # fields = ['username', 'email', 'password1', 'password2']

    #     # help_texts = {
    #     #     'username': '',
    #     #     'email': 'Please enter a valid email address.',  # Custom help text for email
    #     #     'password1': '',
    #     #     'password2': '',
    #     # }
    #     help_texts = {
    #         'username': None,
    #         'password1': None,
    #         'password2': None,
    #     }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(UserRegistrationForm, self).__init__(*args, **kwargs)
    #     if user and user.role == 'admin':
    #         self.fields['role'].choices = [('user', 'User')]


class AdminRegistrationForm(UserCreationForm):
    # email = forms.EmailField(required=True)

    # class Meta:
    #     model = CustomUser
    #     fields = ['username', 'email', 'password1', 'password2']
    #     help_texts = {
    #         'username': None,
    #         'password1': None,
    #         'password2': None,
    #     }

    # def __init__(self, *args, **kwargs):
    #     super(AdminRegistrationForm, self).__init__(*args, **kwargs)
    #     for field_name in ['username', 'password1', 'password2']:
    #         self.fields[field_name].help_text = None
    #         self.fields[field_name].widget.attrs.update({'placeholder': self.fields[field_name].label})
    #     self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs.update({'placeholder': self.fields[field_name].label})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']