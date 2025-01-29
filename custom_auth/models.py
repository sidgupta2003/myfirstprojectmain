from django.contrib.auth.models import AbstractUser
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

ROLE_CHOICES = [
    # ('superadmin', 'Superadmin'),
    ('admin', 'Admin'),
    ('user', 'User'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username