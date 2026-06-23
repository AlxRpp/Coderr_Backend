from django.urls import path
from .views import ListOrCreateOrderView

urlpatterns = [
    path('orders/', ListOrCreateOrderView.as_view(), name='orders')
]
