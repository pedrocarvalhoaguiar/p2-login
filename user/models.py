from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
import pathlib
import uuid

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    def path_to_profile_image(self, filename):
        extension = pathlib.Path(filename).suffix
        new_filename = str(uuid.uuid4()) + extension
        return f'user/images/{new_filename}'

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    points = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    last_login = models.DateTimeField(auto_now=True, null=True)
    profile_image = models.ImageField(upload_to=path_to_profile_image, default='user/images/default-profile.jpg')

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def delete(self):
        self.is_active = False
        super().delete()

    def has_perm(self, perm, obj=None):
        return self.is_admin or self.is_superuser

    def has_module_perms(self, app_label: str) -> bool:
        return True

    def __str__(self):
        return self.name if self.name else self.email


class Card(models.Model):
    user = models.ForeignKey(CustomUser, related_name='card_owner', on_delete=models.DO_NOTHING)
    number = models.CharField(max_length=16, default='')
    flag = models.CharField(max_length=30, choices=(('visa', 'visa'), ('mastercard', 'mastercard'), ('elo', 'elo')),
                            default='visa')

    def __str__(self):
        return self.number


class PaidBill(models.Model):
    card = models.ForeignKey(Card, related_name='card_bill', on_delete=models.DO_NOTHING)
    value = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
