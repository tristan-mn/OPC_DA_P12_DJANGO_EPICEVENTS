from rest_framework.permissions import BasePermission, SAFE_METHODS


class ClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Supports'):
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Sellers'):
            if request.user == obj.sales_contact:
                return True

        if request.user.groups.filter(name='Supports'):
            return request.method in SAFE_METHODS

        if request.user.groups.filter(name='Managers'):
            return True
        return False


class ContractPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Sellers'):
            if request.user == obj.sales_contact:
                return True

        if request.user.groups.filter(name='Managers'):
            return True
        return False


class EventPermissions(BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Supports'):
            if request.user == obj.support_contact:
                return True

        if request.user.groups.filter(name='Managers'):
            return True
        return False