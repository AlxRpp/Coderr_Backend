from django.urls import path
from .views import GetOrCreateOffersView, RetriveUpdateDeleteOfferView, GetOfferDetailsView

urlpatterns = [
    path('offers/', GetOrCreateOffersView.as_view(), name='offers'),
    path('offers/<int:pk>/', RetriveUpdateDeleteOfferView.as_view()),
    path('offerdetails/<int:pk>/', GetOfferDetailsView.as_view(),
         name='offerdetails-detail')
]
