from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    # Avoid conflicts by setting unique related_name values
    # groups = models.ManyToManyField(
    #     "auth.Group",
    #     related_name="customuser_set",
    #     blank=True
    # )
    # user_permissions = models.ManyToManyField(
    #     "auth.Permission",
    #     related_name="customuser_permissions_set",
    #     blank=True
    # )
    
