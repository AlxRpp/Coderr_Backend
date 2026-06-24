from django.contrib import admin
from django.urls import path, include
from .views import CountStatsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('api/', include('auth_app.api.urls')),
    path('api/', include('profile_app.api.urls')),
    path('api/', include('offers_app.api.urls')),
    path('api/', include('orders_app.api.urls')),
    path('api/', include('reviews_app.api.urls')),
    path('api/base-info/', CountStatsView.as_view(), name='base-infos')
]
