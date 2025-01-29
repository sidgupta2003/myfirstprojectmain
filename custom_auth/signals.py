from django.db.models.signals import post_migrate
from django.conf import settings
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com',
            role='superadmin'
        )