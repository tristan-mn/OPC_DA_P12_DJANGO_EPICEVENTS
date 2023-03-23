from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        manager = "Manager"
        seller = "Seller"
        support = "support"

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    role = models.CharField(max_length=64, choices=Role.choices)
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
