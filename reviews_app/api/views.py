from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import GetOrPostReviewSerializer, UpdateOrDeleteReviewSerializer
from ..models import Reviews
from core.permissons import IsCustomerUser, IsReviewOwner
from django.shortcuts import get_object_or_404


class GetOrPostReviewView(ListCreateAPIView):
    """Lists all reviews with optional filtering by business_user_id or reviewer_id.
    Customers can post new reviews via POST."""

    serializer_class = GetOrPostReviewSerializer
    queryset = Reviews.objects.all()

    def get_queryset(self):
        """Supports filtering by business_user_id and reviewer_id. Also allows ordering by updated_at or rating."""
        queryset = Reviews.objects.all()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user=business_user_id)

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer=reviewer_id)

        ordering = self.request.query_params.get('ordering')
        if ordering == 'updated_at':
            queryset = queryset.order_by('updated_at')
        elif ordering == 'rating':
            queryset = queryset.order_by('rating')

        return queryset

    def perform_create(self, serializer):
        """Saves the currently authenticated user as the reviewer before creating the review."""
        serializer.save(
            reviewer=self.request.user
        )

    def get_permissions(self):
        """POST requires the customer role. GET only needs authentication."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]


class UpdateOrDeleteReviewView(RetrieveUpdateDestroyAPIView):
    """Handles GET, PATCH and DELETE for a single review. Only the original reviewer can modify or delete it."""

    serializer_class = UpdateOrDeleteReviewSerializer
    permission_classes = [IsAuthenticated, IsReviewOwner]

    def get_object(self):
        """Fetches the review by pk and runs the IsReviewOwner check before returning it."""
        pk = self.kwargs['pk']
        obj = get_object_or_404(Reviews, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj
