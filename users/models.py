from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default_expiry_time = models.IntegerField(default=30)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
