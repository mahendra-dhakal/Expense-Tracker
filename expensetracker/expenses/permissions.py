from rest_framework import permissions

class IsOwnerOrSuperuser(permissions.BasePermission):
    '''lets only loggedin user or superuser have access/permissions to object'''
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        return request.user.is_superuser or obj.user== request.user