from django.urls import path
from .views import ListOrCreateOrderView, UpdateOrDestoryOrderView, GetOrderInProgressCountView, GetOrderCompletedCountView

urlpatterns = [
    path('orders/', ListOrCreateOrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', UpdateOrDestoryOrderView.as_view(),
         name='orders-details'),
    path('order-count/<int:pk>/', GetOrderInProgressCountView.as_view(),
         name='in-progress-count'),
    path('completed-order-count/<int:pk>/', GetOrderCompletedCountView.as_view(),
         name='completed-count'),
]
