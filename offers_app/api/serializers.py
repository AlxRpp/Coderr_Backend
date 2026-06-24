from rest_framework import serializers
from ..models import Offers, OffersDetails, OffersDetailsFeatures
from django.db.models import Min
from django.contrib.auth import get_user_model

User = get_user_model()


class OffersDetailsSerializer(serializers.ModelSerializer):
    """Serializes a single offer detail tier including its features.
    Features are stored as seperate OffersDetailsFeatures rows but are serialized as a flat list of strings."""

    features = serializers.ListField(
        child=serializers.CharField(), write_only=True)

    def to_representation(self, instance):
        """Replaces the nested features queryset with a flat list of strings and moves offer_type to the end of the response."""
        rep = super().to_representation(instance)
        offer_type = rep.pop('offer_type')
        rep['features'] = list(
            instance.features.values_list('title', flat=True))
        rep['offer_type'] = offer_type
        return rep

    class Meta:
        model = OffersDetails
        fields = ['id', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    """Used for creating and updating offers. Handles the nested details and their features in a single request."""

    details = OffersDetailsSerializer(many=True)

    def create(self, validated_data):
        """Creates the offer, then loops through each detail tier and creates its feature rows.
        Everything happens in one request so the client doesn't need to make seperate calls."""
        details_data = validated_data.pop('details')
        offer = Offers.objects.create(**validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features')
            detail = OffersDetails.objects.create(offers=offer, **detail_data)

            for feature_data in features_data:
                OffersDetailsFeatures.objects.create(
                    offers_detail=detail, title=feature_data)

        return offer

    def update(self, instance, validated_data):
        """Updates the offer's top-level fields and replaces features for each detail tier.
        Existing features are deleted and recreated on every update to keep the logic simple."""
        details_data = validated_data.pop('details', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        for detail_data in details_data:
            features_data = detail_data.pop('features', [])
            offer_type = detail_data.get('offer_type')
            detail = instance.details.get(offer_type=offer_type)

            detail.title = detail_data.get('title', detail.title)
            detail.revisions = detail_data.get('revisions', detail.revisions)
            detail.delivery_time_in_days = detail_data.get(
                'delivery_time_in_days', detail.delivery_time_in_days)
            detail.price = detail_data.get('price', detail.price)
            detail.save()

            detail.features.all().delete()
            for feature in features_data:
                OffersDetailsFeatures.objects.create(
                    offers_detail=detail, title=feature)

        return instance

    class Meta:
        model = Offers
        fields = ['id', 'title', 'image',
                  'description', 'details']


class GetOffersListSerializer(serializers.ModelSerializer):
    """Read-only serializer for the offers list endpoint.
    Adds calculated fields like min_price, min_delivery_time and a short user summary."""

    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_details(self, instance):
        """Returns only the id and url for each detail tier instead of the full nested objects."""
        return [{"id": details.id, "url": f"/offerdetails/{details.id}/"}
                for details in instance.details.all()]

    def get_min_price(self, instance):
        """Returns the cheapest price accross all detail tiers of this offer using a database aggregate."""
        result = instance.details.aggregate(min_price=Min('price'))
        return result['min_price']

    def get_min_delivery_time(self, instance):
        """Returns the shortest delivery time across all detail tiers using a database aggregate."""
        result = instance.details.aggregate(
            min_delivery_time=Min('delivery_time_in_days'))
        return result['min_delivery_time']

    def get_user_details(self, instance):
        """Returns a short summary of the offer creator with first name, last name and username."""
        user = instance.user

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username
        }

    class Meta:
        model = Offers
        fields = ['id', 'user', 'title', 'image',
                  'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    """Minimal serializer that provides just the id and a hyperlink for a single offer detail tier."""

    url = serializers.HyperlinkedIdentityField(view_name='offerdetails-detail')

    class Meta:
        model = OffersDetails
        fields = ['id', 'url']


class GetOfferDetailSerializer(serializers.ModelSerializer):
    """Read-only serializer for a full offer including nested detail links and calculated min values."""

    details = OfferDetailLinkSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    def get_min_price(self, instance):
        """Calculates the minimum price by agregating over all related OffersDetails objects."""
        result = instance.details.aggregate(min_price=Min('price'))
        return result['min_price']

    def get_min_delivery_time(self, instance):
        """Calculates the minimum delivery time across all related OffersDetails objects."""
        result = instance.details.aggregate(
            min_delivery_time=Min('delivery_time_in_days'))
        return result['min_delivery_time']

    class Meta:
        model = Offers
        fields = ['id', 'user', 'title', 'image',
                  'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
