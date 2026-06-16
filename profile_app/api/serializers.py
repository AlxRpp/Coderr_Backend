from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class ProfilSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='pk')
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='pk', read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = User
        extra_kwargs = {
            'user': {'read_only': True},
            'username': {'read_only': True},
            'file': {'read_only': True},
            'type': {'read_only': True}
        }

        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class GetProfileTypeListSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']
