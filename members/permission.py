from rest_framework.permissions import BasePermission


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user and (request.user.group.filter(name="is_member") or request.user.group.filter(name="is_user")):
            return True
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.group.filter(name="is_user"):
            return True
        return False
