from django.apps import AppConfig
from django.db.models.signals import post_migrate   #new


class CustomAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'



    # for  superuser
    def ready(self):
        import custom_auth.signals
