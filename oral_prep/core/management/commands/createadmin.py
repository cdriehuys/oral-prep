import os

from allauth.account.models import EmailAddress
from django.core.management.base import BaseCommand, CommandError

from core import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        email = os.environ.get("ORALPREP_ADMIN_EMAIL")

        if not email:
            raise CommandError(
                "The environment variable 'ORALPREP_ADMIN_EMAIL' must be set."
            )

        try:
            email = EmailAddress.objects.filter(email=email).get()
            if email.user.is_superuser:
                self.stdout.write("Admin user already exists.")
                return
            else:
                raise CommandError(
                    f"A user with the email '{email}' already exists, but they are not an admin."
                )
        except EmailAddress.DoesNotExist:
            user = models.User.objects.create_superuser(email=email)
            EmailAddress.objects.create(
                user=user,
                email=email,
                verified=True,
                primary=True,
            )

            self.stdout.write(
                self.style.SUCCESS(f"Created admin user with email '{email}'.")
            )
            self.stdout.write(
                "Use the password reset function to change the admin password."
            )
