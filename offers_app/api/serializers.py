from rest_framework import serializers
from django.db.models import Min
from ..models import Offers, OffersDetails, OffersDetailsFeatures
from django.contrib.auth import get_user_model
User = get_user_model()


class OffersDetailsSerializer(serializers.ModelSerializer):
    features = serializers.ListField(
        child=serializers.CharField(), write_only=True)

    def to_representation(self, instance):
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
    details = OffersDetailsSerializer(many=True)

    def create(self, validated_data):
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
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    def get_details(self, instance):
        return [{"id": details.id, "url": f"/offerdetails/{details.id}/"}
                for details in instance.details.all()]

    def get_min_price(self, instance):
        result = instance.details.aggregate(min_price=Min('price'))
        return result['min_price']

    def get_min_delivery_time(self, instance):
        result = instance.details.aggregate(
            min_delivery_time=Min('delivery_time_in_days'))
        return result['min_delivery_time']

    def get_user_details(self, instance):
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
    url = serializers.HyperlinkedIdentityField(view_name='offerdetails-detail')

    class Meta:
        model = OffersDetails
        fields = ['id', 'url']


class GetOfferDetailSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    def get_min_price(self, instance):
        result = instance.details.aggregate(min_price=Min('price'))
        return result['min_price']

    def get_min_delivery_time(self, instance):
        result = instance.details.aggregate(
            min_delivery_time=Min('delivery_time_in_days'))
        return result['min_delivery_time']

    class Meta:
        model = Offers
        fields = ['id', 'user', 'title', 'image',
                  'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
