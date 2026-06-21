from rest_framework import serializers
from ..models import Offers, OffersDetails, OffersDetailsFeatures


# class OffersDetailsFeaturesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OffersDetailsFeatures
#         fields = ['title']


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

    class Meta:
        model = Offers
        fields = ['id', 'title', 'image',
                  'description', 'details']
