from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


User = get_user_model()


class Reviews(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='business_user_reviews')
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer')
    rating = models.IntegerField(null=False, blank=False,
                                 validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reviewer}"

    class Meta:
        unique_together = ('reviewer', 'business_user')
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['id']
