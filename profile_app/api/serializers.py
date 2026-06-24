from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfilSerializer(serializers.ModelSerializer):
    """Read serializer for a user profile. Returns all public profile fields including contact info and timestamps."""

    user = serializers.IntegerField(source='pk')
    created_at = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M:%SZ", read_only=True)

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):
    """Write serializer for updating a user profile.
    Sensitive fields like username, file and type are locked to read-only so they can't be changed here."""

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


class GetProfileTypeBusinessListSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing business profiles. Excludes private fields like email and timestamps."""

    user = serializers.IntegerField(source='pk', read_only=True)

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name', 'last_name', 'file',
                  'location', 'tel', 'description', 'working_hours', 'type']


class GetProfileTypeListCustomerSerializer(serializers.ModelSerializer):
    """Minimal serializer for listing customer profiles.
    Includes the file upload timestamp instead of the account creation date."""

    user = serializers.IntegerField(source='pk', read_only=True)
    uploaded_at = serializers.DateTimeField(
        source='file_uploaded_at', format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ['user', 'username', 'first_name',
                  'last_name', 'file', 'uploaded_at', 'type']
