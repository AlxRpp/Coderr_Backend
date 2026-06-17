from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .serializers import ProfilSerializer, UpdateProfileSerializer, GetProfileTypeBusinessListSerializer, GetProfileTypeListCustomerSerializer
from core.permissons import IsOwner
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()


class GetDetailProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfilSerializer
        return UpdateProfileSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class GetProfileTypeBusinessListView(ListAPIView):
    serializer_class = GetProfileTypeBusinessListSerializer

    def get_queryset(self):
        obj = User.objects.filter(type='business')
        return obj


class GetProfileTypeCustomerListView(ListAPIView):
    serializer_class = GetProfileTypeListCustomerSerializer

    def get_queryset(self):
        obj = User.objects.filter(type='customer')
        return obj
