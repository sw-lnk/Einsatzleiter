from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=False)
    first_name = models.CharField(_("first name"), null=False)
    last_name = models.CharField(_("last name"), null=False)

    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    # objects = CustomUserManager()

    def __str__(self):
        return self.email
