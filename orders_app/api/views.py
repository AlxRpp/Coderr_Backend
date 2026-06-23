from rest_framework.generics import ListCreateAPIView
from .serializers import ListOrCreateOrderSerializer
from ..models import Orders
from core.permissons import IsCustomerUser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


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
