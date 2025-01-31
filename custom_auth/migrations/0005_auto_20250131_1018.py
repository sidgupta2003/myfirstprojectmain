# filepath: /C:/Users/BPIN/OneDrive/Desktop/abc/myfirstproject/custom_auth/migrations/0005_auto_add_roles.py
from django.db import migrations

def create_roles(apps, schema_editor):
    Role = apps.get_model('custom_auth', 'Role')
    Role.objects.create(name='superadmin')
    Role.objects.create(name='admin')
    Role.objects.create(name='user')

class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_role_alter_customuser_role'),
    ]

    operations = [
        migrations.RunPython(create_roles),
    ]