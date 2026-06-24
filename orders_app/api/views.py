from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import ListOrCreateOrderSerializer, UpdateOrderSerializer
from ..models import Orders
from core.permissons import IsCustomerUser, IsBusinessUser, IsOwnerOrAdmin
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class ListOrCreateOrderView(ListCreateAPIView):
    """Lists orders for the current user and allows customers to place new orders."""

    queryset = Orders.objects.all()
    serializer_class = ListOrCreateOrderSerializer
    permission_classes = [IsCustomerUser]

    def perform_create(self, serializer):
        """Looks up the business_user from the chosen offer detail and saves them alongside the customer_user."""
        offer_detail = serializer.validated_data.get('offer_detail_id')
        business_user = offer_detail.offers.user
        serializer.save(
            customer_user=self.request.user,
            business_user=business_user
        )

    def get_permissions(self):
        """POST requires the customer role. GET only requires authentication."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """Returns only orders where the current user is either the customer or the business side."""
        return Orders.objects.filter(Q(customer_user=self.request.user) | Q(business_user=self.request.user))


class UpdateOrDestoryOrderView(RetrieveUpdateDestroyAPIView):
    """Allows updating the order status (business users only) or deleting an order (admin or owner)."""

    serializer_class = UpdateOrderSerializer
    queryset = Orders.objects.all()

    def get_permissions(self):
        """PATCH is restricted to business users. Everything else requires authentication and admin or ownership."""
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUser()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


class GetOrderInProgressCountView(APIView):
    """Returns the number of in_progress orders for a given business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Validates that the user exists and counts their currently active orders."""
        if not User.objects.filter(pk=pk).exists():
            raise NotFound()
        count = Orders.objects.filter(
            business_user=pk,
            status='in_progress').count()
        return Response({'order_count': count})


class GetOrderCompletedCountView(APIView):
    """Returns the number of completed orders for a given business user."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Validates that the user exists and counts all their orders with status 'completed'."""
        if not User.objects.filter(pk=pk).exists():
            raise NotFound()
        count = Orders.objects.filter(
            business_user=pk,
            status='completed').count()
        return Response({'completed_order_count': count})
