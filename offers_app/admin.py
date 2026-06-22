from django.contrib import admin
from .models import Offers, OffersDetails, OffersDetailsFeatures

# Register your models here.
admin.site.register(Offers)
admin.site.register(OffersDetails)
admin.site.register(OffersDetailsFeatures)
