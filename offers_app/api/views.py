from .serializers import OfferSerializer, GetOffersListSerializer, GetOfferDetailSerializer, OffersDetailsSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from ..models import Offers, OffersDetails
from core.permissons import IsBusinessUser, IsOfferOwner
from django.shortcuts import get_object_or_404
from django.db.models import Min


class OfferPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'


class GetOrCreateOffersView(ListCreateAPIView):
    queryset = Offers.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Offers.objects.annotate(
            min_price_val=Min('details__price'),
            min_delivery_val=Min('details__delivery_time_in_days')
        )

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user__id=creator_id)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(min_price_val__gte=min_price)

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            queryset = queryset.filter(min_delivery_val__lte=max_delivery_time)

        ordering = self.request.query_params.get('ordering')
        if ordering == 'min_price':
            queryset = queryset.order_by('min_price_val')
        elif ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetOffersListSerializer
        return OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessUser()]


class RetriveUpdateDeleteOfferView(RetrieveUpdateDestroyAPIView):
    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(Offers, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetOfferDetailSerializer
        elif self.request.method == 'PATCH':
            return OfferSerializer
        else:
            return OfferSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOfferOwner()]
        else:
            return [IsAuthenticated(), IsOfferOwner()]


class GetOfferDetailsView(RetrieveAPIView):
    serializer_class = OffersDetailsSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(OffersDetails, pk=pk)
        return obj
