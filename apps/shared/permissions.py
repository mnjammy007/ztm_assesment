from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Superuser: full access
    Admin (is_staff): read-only access to all objects
    Normal user: can access only their own objects
    """

    def has_permission(self, request, view):
        # Must be authenticated (IsAuthenticated should also be used)
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Superuser → full access
        if user.is_superuser:
            return True

        # Admin → read-only access
        if user.is_staff:
            return request.method in SAFE_METHODS

        # Normal user ownership checks note that Task model (has foreign key to user)
        if hasattr(obj, "user"):
            return obj.user == user

        # User model (object itself is the user)
        return obj == user
