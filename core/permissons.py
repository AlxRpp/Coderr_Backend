from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

user = get_user_model()


class IsOwnerOrAdmin(BasePermission):
    """Grants access only to superusers. Usefull for operations that should be strictly admin-only."""

    def has_object_permission(self, request, view, obj):
        """Returns True only if the requesting user is a superuser."""
        is_admin = bool(request.user and request.user.is_superuser)
        return is_admin


class IsOwner(BasePermission):
    """Grants read access to everyone but restricts write access to the user who owns the object."""

    def has_object_permission(self, request, view, obj):
        """Safe methods are always allowed. Anything else requires the request user to be the object itself."""
        is_owner = bool(request.user and request.user == obj)

        if request.method in SAFE_METHODS:
            return True
        else:
            return is_owner


class IsOfferOwner(BasePermission):
    """Grants read access to everyone but restricts modifications to the user who created the offer."""

    def has_object_permission(self, request, view, obj):
        """Checks wether the request user matches the offer's creator field."""
        is_owner = bool(request.user and request.user == obj.user)

        if request.method in SAFE_METHODS:
            return True
        else:
            return is_owner


class IsReviewOwner(BasePermission):
    """Restricts editing and deleting a review to the user who originally wrote it."""

    def has_object_permission(self, request, view, obj):
        """Read access is open to everyone. Write access is limited to the reviewer."""
        is_owner = bool(request.user and request.user == obj.reviewer)

        if request.method in SAFE_METHODS:
            return True
        else:
            return is_owner


class IsBusinessUser(BasePermission):
    """Allows access only to users whose type field is set to 'business'."""

    def has_permission(self, request, view):
        """Checks the type field on the CustomUser model."""
        is_business_user = bool(request.user.type == 'business')
        return is_business_user


class IsCustomerUser(BasePermission):
    """Allows access only to users whose type field is set to 'customer'."""

    def has_permission(self, request, view):
        """Checks the type field on the CustomUser model."""
        is_business_user = bool(request.user.type == 'customer')
        return is_business_user
