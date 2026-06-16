from django.urls import path
from .views import GetDetailProfileView, GetProfileTypeListView

urlpatterns = [
    path('profile/<int:pk>/', GetDetailProfileView.as_view(),
         name='profil-detail-view'),
    path('profiles/business/', GetProfileTypeListView.as_view(profile_type='business')),
    path('profiles/customer/', GetProfileTypeListView.as_view(profile_type='customer')),

]
