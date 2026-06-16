from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    type_choices = [
        ('customer', 'Customer'),
        ('business', 'Business')
    ]

    type = models.CharField(choices=type_choices, max_length=50)

    def __str__(self):
        return f"{self.username}, {self.email}, {self.type}"
