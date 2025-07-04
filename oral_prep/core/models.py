from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):

    def create_user(self, email: str, password: str = None) -> "User":
        user = User(email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email: str, password: str = None) -> "User":
        user = User(email=email, is_staff=True, is_superuser=True)
        user.set_password(password)
        user.save()

        return user


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True, verbose_name=_("email"))

    is_staff = models.BooleanField(default=False, verbose_name=_("is staff"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("is superuser"))

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    objects = UserManager()

    @property
    def is_active(self):
        return True
