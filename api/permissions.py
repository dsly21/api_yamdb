from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user.is_staff and
            request.user.is_authenticated
        )


class IsAdminOrAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return(
                request.method in permissions.SAFE_METHODS or
                request.user == obj.author or
                request.user.is_moderator and
                request.user.is_authenticated or
                request.user.is_admin)


class IsAdminPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin
