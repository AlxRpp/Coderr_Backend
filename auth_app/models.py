from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    type_choices = [
        ('customer', 'Customer'),
        ('business', 'Business')
    ]
    first_name = models.CharField(
        max_length=255, blank=True, null=False, default="")
    last_name = models.CharField(
        max_length=255, blank=True, null=False, default="")
    file = models.FileField(upload_to='uploads/',
                            max_length=100, null=True)
    location = models.CharField(
        max_length=255, blank=True, null=False, default="")
    tel = models.CharField(max_length=20, blank=True, null=False, default="")
    description = models.TextField(blank=True, null=False, default="")
    working_hours = models.TextField(blank=True, null=False, default="")
    type = models.CharField(choices=type_choices, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} | {self.first_name}  {self.last_name} | {self.type}"
