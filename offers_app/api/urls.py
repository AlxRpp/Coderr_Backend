from django.urls import path
from .views import PostOfferView

urlpatterns = [
    path('offers/', PostOfferView.as_view(), name='post-offer')
]
