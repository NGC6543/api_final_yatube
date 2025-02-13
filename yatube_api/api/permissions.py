from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly,
                        permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            (request.method in permissions.SAFE_METHODS) or
            (obj.author == request.user)
        )
