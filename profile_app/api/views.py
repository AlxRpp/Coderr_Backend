from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from .serializers import ProfilSerializer, UpdateProfileSerializer, GetProfileTypeListSerializer
from core.permissons import IsOwnerOrAdmin
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()


class GetDetailProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProfilSerializer
        return UpdateProfileSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj


class GetProfileTypeListView(ListAPIView):
    serializer_class = GetProfileTypeListSerializer
    profile_type = None

    def get_queryset(self):
        obj = User.objects.filter(type=self.profile_type)
        return obj
