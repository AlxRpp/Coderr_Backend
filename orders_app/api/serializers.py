from rest_framework import serializers
from ..models import Orders
from offers_app.api.serializers import OffersDetailsSerializer
from offers_app.models import OffersDetails


class ListOrCreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating orders.
    On read, the nested offer detail fields are flattened into the top-level response so the client gets everything in one place."""

    offer_detail = OffersDetailsSerializer(read_only=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    offer_detail_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=True,
        queryset=OffersDetails.objects.all())
    customer_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        required=False
    )
    business_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        required=False
    )

    def create(self, validated_data):
        """Extracts offer_detail_id and creates the order. customer_user and business_user are set by the view."""
        offer_detail = validated_data.pop('offer_detail_id')
        return Orders.objects.create(offer_detail=offer_detail, **validated_data)

    def to_representation(self, instance):
        """Flattens the nested offer_detail object into the top-level response and enforces a fixed field order."""
        rep = super().to_representation(instance)
        offer_detail = rep.pop('offer_detail')

        for key in ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']:
            rep[key] = offer_detail.get(key)

        order = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                 'delivery_time_in_days', 'price', 'features', 'offer_type',
                 'status', 'created_at', 'updated_at']

        result = {}
        for key in order:
            result[key] = rep[key]
        return result

    class Meta:
        model = Orders
        fields = ['id', 'customer_user', 'business_user', 'offer_detail',
                  'status', 'created_at', 'updated_at', 'offer_detail_id']


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Serializer for updating an existing order. Offer detail fields and user references are read-only here."""

    class Meta:
        model = Orders
        fields = ['id', 'customer_user', 'business_user', 'offer_detail',
                  'status', 'created_at', 'updated_at']

    offer_detail = OffersDetailsSerializer(read_only=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    customer_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    business_user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    def to_representation(self, instance):
        """Same flattening logic as ListOrCreateOrderSerializer — merges offer detail fields into the top-level response."""
        rep = super().to_representation(instance)
        offer_detail = rep.pop('offer_detail')

        for key in ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']:
            rep[key] = offer_detail.get(key)

        order = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                 'delivery_time_in_days', 'price', 'features', 'offer_type',
                 'status', 'created_at', 'updated_at']

        result = {}
        for key in order:
            result[key] = rep[key]
        return result
