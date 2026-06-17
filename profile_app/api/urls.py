from django.urls import path
from .views import GetDetailProfileView, GetProfileTypeBusinessListView, GetProfileTypeCustomerListView

urlpatterns = [
    path('profile/<int:pk>/', GetDetailProfileView.as_view(),
         name='profil-detail-view'),
    path('profiles/business/',
         GetProfileTypeBusinessListView.as_view(), name='type_business'),
    path('profiles/customer/', GetProfileTypeCustomerListView.as_view(),
         name='type_customer')

]
