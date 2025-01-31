# filepath: /C:/Users/BPIN/OneDrive/Desktop/abc/myfirstproject/custom_auth/migrations/0007_auto_add_superadmin.py
from django.db import migrations

def create_superadmin(apps, schema_editor):
    Role = apps.get_model('custom_auth', 'Role')
    Admin = apps.get_model('custom_auth', 'Admin')
    superadmin_role = Role.objects.get(name='superadmin')
    Admin.objects.create(
        role=superadmin_role,
        username='superadmin',
        email='superadmin@example.com',
        password='superadminpassword'  # Note: In a real application, ensure passwords are hashed
    )

class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0006_admin'),
    ]

    operations = [
        migrations.RunPython(create_superadmin),
    ]