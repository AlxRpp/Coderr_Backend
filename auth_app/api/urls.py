from django.urls import path
from .views import RegistrationView, LoginUserView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login')

]
