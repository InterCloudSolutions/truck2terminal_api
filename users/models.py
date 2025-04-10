from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    DRIVER = "driver"
    TERMINAL_MANAGER = "terminal_manager"
    ADMIN = "admin"

    ROLE_CHOICES = [
        (DRIVER, "Driver"),
        (TERMINAL_MANAGER, "Terminal Manager"),
        (ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=DRIVER)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

