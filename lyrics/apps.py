from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


class LyricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lyrics"

    def ready(self):
        from django.contrib.auth.models import User  # Import inside ready to avoid early ORM usage

        def create_admin_user(sender, **kwargs):
            """
            Create a superuser automatically after migrations if one doesn't already exist.
            """
            username = os.getenv("ADMIN_USERNAME")
            email = os.getenv("ADMIN_EMAIL")
            password = os.getenv("ADMIN_PASSWORD")

            if username and email and password:
                if not User.objects.filter(username=username).exists():
                    User.objects.create_superuser(username=username, email=email, password=password)
                    print(f"Superuser {username} created.")
                else:
                    print(f"Superuser {username} already exists.")

        # Connect the post_migrate signal
        post_migrate.connect(create_admin_user, sender=self)