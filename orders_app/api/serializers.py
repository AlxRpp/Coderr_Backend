from rest_framework import serializers
from ..models import Orders
from offers_app.api.serializers import OffersDetailsSerializer
from offers_app.models import Offers, OffersDetails


class ListOrCreateOrderSerializer(serializers.ModelSerializer):
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
        offer_detail = validated_data.pop('offer_detail_id')
        return Orders.objects.create(offer_detail=offer_detail, **validated_data)

    def to_representation(self, instance):
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
