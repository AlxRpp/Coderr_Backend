from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
user = get_user_model()


# class IsStaffOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         isStaff = bool(request.user and request.user.is_staff)
#         return isStaff or request.method in SAFE_METHODS


# class hasTheLastname(BasePermission):
#     def has_permission(self, request, view):
#         lastname = bool(request.user and request.user.last_name == "hallo")
#         return lastname or request.method in SAFE_METHODS


# class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         elif request.method == "DELETE":
#             return bool(request.user and request.user.is_superuser)
#         else:
#             return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = bool(request.user and request.user.is_superuser)
        is_owner = bool(request.user and request.user == obj)

        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return is_admin
        else:
            return is_admin or is_owner
