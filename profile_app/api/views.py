from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .serializers import ProfilSerializer, UpdateProfileSerializer, GetProfileTypeBusinessListSerializer, GetProfileTypeListCustomerSerializer
from core.permissons import IsOwner
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()


class GetDetailProfileView(RetrieveUpdateAPIView):
    """Handles GET and PATCH for a single user profile. Only the profile owner can make changes."""

    permission_classes = [IsOwner]

    def get_serializer_class(self):
        """GET returns the full read serializer. PATCH uses the restricted update serializer."""
        if self.request.method == 'GET':
            return ProfilSerializer
        return UpdateProfileSerializer

    def get_object(self):
        """Fetches the user by pk and runs the IsOwner permission check before returning the object."""
        pk = self.kwargs['pk']
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class GetProfileTypeBusinessListView(ListAPIView):
    """Returns a list of all users with type 'business'."""

    serializer_class = GetProfileTypeBusinessListSerializer

    def get_queryset(self):
        """Filters the user queryset to only include business type accounts."""
        obj = User.objects.filter(type='business')
        return obj


class GetProfileTypeCustomerListView(ListAPIView):
    """Returns a list of all users with type 'customer'."""

    serializer_class = GetProfileTypeListCustomerSerializer

    def get_queryset(self):
        """Filters the user queryset to only include customer type accounts."""
        obj = User.objects.filter(type='customer')
        return obj
