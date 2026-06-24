from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from .serializers import OfferSerializer, GetOffersListSerializer, GetOfferDetailSerializer, OffersDetailsSerializer
from ..models import Offers, OffersDetails
from django_filters.rest_framework import DjangoFilterBackend
from core.permissons import IsBusinessUser, IsOfferOwner
from django.shortcuts import get_object_or_404
from django.db.models import Min


class OfferPagination(PageNumberPagination):
    """Pagination config for the offers list. Defaults to 2 items per page."""

    page_size = 2
    page_size_query_param = 'page_size'


class GetOrCreateOffersView(ListCreateAPIView):
    """Lists all offers with optional filtering and search. Business users can create new offers via POST."""

    queryset = Offers.objects.all()
    pagination_class = OfferPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_queryset(self):
        """Builds the queryset with annotations for min_price and min_delivery_time so filtering by those values is possible."""
        queryset = Offers.objects.annotate(
            min_price_val=Min('details__price'),
            min_delivery_val=Min('details__delivery_time_in_days')
        )

        creator_id = self.request.query_params.get('creator_id')
        if creator_id:
            queryset = queryset.filter(user__id=creator_id)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(min_price_val__gte=float(min_price))
            except (ValueError, TypeError):
                pass

        max_delivery_time = self.request.query_params.get('max_delivery_time')
        if max_delivery_time:
            try:
                queryset = queryset.filter(min_delivery_val__lte=int(max_delivery_time))
            except (ValueError, TypeError):
                pass

        ordering = self.request.query_params.get('ordering')
        if ordering == 'min_price':
            queryset = queryset.order_by('min_price_val')
        elif ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')

        return queryset

    def perform_create(self, serializer):
        """Attaches the logged in user as the owner of the new offer before saving."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """GET uses the detailed list serializer. POST uses the write serializer."""
        if self.request.method == 'GET':
            return GetOffersListSerializer
        return OfferSerializer

    def get_permissions(self):
        """Everyone can browse offers but only authenticated business users can create them."""
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessUser()]


class RetriveUpdateDeleteOfferView(RetrieveUpdateDestroyAPIView):
    """Handles GET, PATCH and DELETE for a single offer by its pk."""

    def get_object(self):
        """Fetches the offer by pk and runs object-level permission checks before returning it."""
        pk = self.kwargs['pk']
        obj = get_object_or_404(Offers, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        """GET uses the detail serializer. PATCH and DELETE both use the write serializer."""
        if self.request.method == 'GET':
            return GetOfferDetailSerializer
        elif self.request.method == 'PATCH':
            return OfferSerializer
        else:
            return OfferSerializer

    def get_permissions(self):
        """GET requires authentication. PATCH and DELETE also require the user to be the offer owner."""
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated(), IsOfferOwner()]
        else:
            return [IsAuthenticated(), IsOfferOwner()]


class GetOfferDetailsView(RetrieveAPIView):
    """Returns a single OffersDetails object (one pricing tier) by its pk."""

    serializer_class = OffersDetailsSerializer

    def get_object(self):
        """Fetches the offer detail by pk. Returns 404 if it doesn't exist."""
        pk = self.kwargs['pk']
        obj = get_object_or_404(OffersDetails, pk=pk)
        return obj
