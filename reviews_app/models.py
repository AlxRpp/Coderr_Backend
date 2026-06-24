from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Reviews(models.Model):
    """Stores a review that a customer leaves for a business user.
    The unique_together constraint ensures a reviewer can only review each business user once."""

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
