from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(
        self, email, password, is_superuser=False, **extra_fields
    ):
        email = self.normalize_email(email)
        user = self.model(
            email=email, is_superuser=is_superuser, **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(
            email, password, is_superuser=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=150, null=False, blank=False, unique=True
    )
    phone_number = models.IntegerField(
        null=False, blank=False, default=702260027
    )
    address_line_1 = models.CharField(
        max_length=255, null=False, blank=False, default=""
    )
    address_line_2 = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
