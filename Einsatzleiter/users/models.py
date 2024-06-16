from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=False)
    first_name = models.CharField(_("first name"), max_length=50, null=False)
    last_name = models.CharField(_("last name"), max_length=50, null=False)

    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["email"]

    # objects = CustomUserManager()

    def name(self):
        if self.first_name and self.last_name:
            return f'{self.last_name}, {self.first_name}'
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return '?, ?'
    
    def __str__(self):
        return self.username
