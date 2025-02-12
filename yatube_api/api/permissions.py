from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
            )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class OnlyAuthorHasPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class CanSeeFollow(permissions.BasePermission):
    def has_permission(self, request, view):
        # print(dir(view))
        # print(view.get_queryset)
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        # if request.user == obj.user:
        #     return True
        # print(obj.user, request.user)
        return obj.user == request.user
