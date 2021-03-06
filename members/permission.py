from rest_framework.permissions import BasePermission


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.groups.filter(name="is_member") or request.user.groups.filter(name="is_admin") or request.user.groups.filter(name="is_super_user"):
                return True
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.groups.filter(name="is_admin") or request.user.groups.filter(name="is_super_user"):
                return True
        return False

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.groups.filter(name="is_super_user"):
                return True
        return False


class IsSiteEditor(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.groups.filter(name="is_super_user") or request.user.groups.filter(name="is_site_editor"):
                return True
        return False


class UserIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id:
            return True