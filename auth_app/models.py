from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    """Extended user model that adds profile fields and a type field (customer or business).
    This is the main user model used across the entire project."""

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
    file_uploaded_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """Overrides default save to automatically update file_uploaded_at whenever the profile image changes."""
        if self.pk:
            old = CustomUser.objects.get(pk=self.pk)
            if old.file != self.file:
                self.file_uploaded_at = timezone.now()
        else:
            if self.file:
                self.file_uploaded_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} | {self.first_name}  {self.last_name} | {self.type}"
