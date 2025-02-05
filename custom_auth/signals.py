from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.conf import settings
from django.dispatch import receiver
from .models import CustomUser, Admin, Role, User

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com',
            role='superadmin'
        )

@receiver(post_save, sender=CustomUser)
def create_admin(sender, instance, created, **kwargs):
    if created and instance.role == 'admin':
        admin_role = Role.objects.get(name='admin')
        Admin.objects.create(
            role=admin_role,
            username=instance.username,
            email=instance.email,
            password=instance.password  
        )

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if not CustomUser.objects.filter(is_superuser=True).exists():
        CustomUser.objects.create_superuser(
            username='admin',
            password='admin',
            email='admin@example.com',
            role='superadmin'
        )


# @receiver(post_save, sender=CustomUser)
# def create_user(sender, instance, created, **kwargs):
#     if created and instance.role == 'user':
#         admin = Admin.objects.get(username=instance.created_by.username)  
#         User.objects.create(
#             admin=admin,
#             username=instance.username,
#             email=instance.email,
#             password=instance.password  
#         )

@receiver(post_save, sender=CustomUser)
# def create_user(sender, instance, created, **kwargs):
#     if created and instance.role == 'user' and instance.created_by and instance.created_by.role in ['admin', 'superadmin']:
#         try:
#             admin = Admin.objects.get(username=instance.created_by.username)
#             User.objects.create(
#                 admin_id=admin.id,
#                 username=instance.username,
#                 email=instance.email,
#                 password=instance.password
#             )
#         except Admin.DoesNotExist:
#             # Handle the case where the Admin object does not exist
#             pass

def create_user(sender, instance, created, **kwargs):
    if created and instance.role == 'user' and instance.created_by:
        try:
            admin = Admin.objects.get(username=instance.created_by.username)
            User.objects.create(
                admin_id=admin.id,
                username=instance.username,
                email=instance.email,
                password=instance.password
            )
        except Admin.DoesNotExist:
            # Handle the case where the Admin object does not exist
            pass