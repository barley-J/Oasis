from rest_framework import permissions


class IsSelf(permissions.BasePermission):
    """
    检测当前操作的用户是否是自己
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user