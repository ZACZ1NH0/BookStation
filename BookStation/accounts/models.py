from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    phone = models.CharField(max_length=12, unique=True)
    def __str__(self):
        return self.username

