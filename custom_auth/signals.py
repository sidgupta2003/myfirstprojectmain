from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    """
    Automatically reset or create a superuser when the database is migrated.
    """
    superuser_email = "admin@example.com"
    superuser_username = "admin"
    superuser_password = "admin1234"

    if not User.objects.filter(is_superuser=True).exists():
        print("No superuser found. Creating default superuser...")
        User.objects.create_superuser(
            username=superuser_username,
            email=superuser_email,
            password=superuser_password
        )
        print(f"Superuser created with username: '{superuser_username}' and password: '{superuser_password}'")
    else:
        print("Superuser already exists. Skipping creation.")
