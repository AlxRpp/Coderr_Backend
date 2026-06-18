from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Offers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    image = models.FileField(upload_to='uploads/offers_img/', null=True)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['id']


class OffersDetails(models.Model):
    OFFER_DETAIL_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]

    offers = models.ForeignKey(Offers, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    revisions = models.IntegerField(blank=False, null=False)
    delivery_time_in_days = models.IntegerField(blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    offer_type = models.CharField(choices=OFFER_DETAIL_CHOICES, max_length=50)

    def __str__(self):
        return f"{self.title} | {self.offer_type}"

    class Meta:
        verbose_name = 'Offer-Detail',
        verbose_name_plural = 'Offers-Details'
        ordering = ['id']
        unique_together = ('offers', 'offer_type')


class OffersDetailsFeatures(models.Model):
    offers_detail = models.ForeignKey(OffersDetails, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Feature_Title',
        verbose_name_plural = 'Feature_Titles'
        ordering = ['id']
