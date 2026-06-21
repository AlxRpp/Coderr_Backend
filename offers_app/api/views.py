from .serializers import OfferSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from ..models import Offers
from core.permissons import IsBusinessUser


class PostOfferView(CreateAPIView):
    serializer_class = OfferSerializer
    # queryset = Offers.objects.all()
    permission_classes = [IsAuthenticated, IsBusinessUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
