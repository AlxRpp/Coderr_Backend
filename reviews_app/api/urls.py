from django.urls import path
from .views import GetOrPostReviewView, UpdateOrDeleteReviewView
urlpatterns = [
    path('reviews/', GetOrPostReviewView.as_view(), name='review'),
    path('reviews/<int:pk>/', UpdateOrDeleteReviewView.as_view(), name='review-detail')
]
