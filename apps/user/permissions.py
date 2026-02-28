from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # The user must be the owner of the object
        return obj == request.user
