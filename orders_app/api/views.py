from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import ListOrCreateOrderSerializer, UpdateOrderSerializer
from ..models import Orders
from core.permissons import IsCustomerUser, IsBusinessUser, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from django.db.models import Q
User = get_user_model()


class ListOrCreateOrderView(ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = ListOrCreateOrderSerializer
    permission_classes = [IsCustomerUser]

    def perform_create(self, serializer):
        offer_detail = serializer.validated_data.get('offer_detail_id')
        business_user = offer_detail.offers.user
        serializer.save(
            customer_user=self.request.user,
            business_user=business_user
        )

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return Orders.objects.filter(Q(customer_user=self.request.user) | Q(business_user=self.request.user))


class UpdateOrDestoryOrderView(RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateOrderSerializer
    queryset = Orders.objects.all()

    def get_permissions(self):
        if self.request.method == 'PATCH':
            return [IsAuthenticated(), IsBusinessUser()]
        return [IsAuthenticated(), IsOwnerOrAdmin()]


class GetOrderInProgressCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not User.objects.filter(pk=pk).exists():
            raise NotFound()
        count = Orders.objects.filter(
            business_user=pk,
            status='in_progress').count()
        return Response({'order_count': count})


class GetOrderCompletedCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if not User.objects.filter(pk=pk).exists():
            raise NotFound()
        count = Orders.objects.filter(
            business_user=pk,
            status='completed').count()
        return Response({'completed_order_count': count})
