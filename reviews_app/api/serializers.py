
from rest_framework import serializers
from ..models import Reviews
from django.contrib.auth import get_user_model
User = get_user_model()


class GetOrPostReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type='business'))
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
    description = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)

    class Meta:
        model = Reviews
        unique_together = ('reviewer', 'business_user')
        fields = ['id', 'business_user', 'reviewer',
                  'rating', 'description', 'created_at', 'updated_at']


class UpdateOrDeleteReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
    description = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%dT%H:%M:%SZ', read_only=True)

    class Meta:
        model = Reviews
        fields = ['id', 'business_user', 'reviewer',
                  'rating', 'description', 'created_at', 'updated_at']
