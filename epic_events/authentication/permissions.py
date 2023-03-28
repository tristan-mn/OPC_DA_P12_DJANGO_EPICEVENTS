from rest_framework.permissions import BasePermission, SAFE_METHODS
from crm.models import Event, Client

owner_methods = ("PUT", "DELETE")


class ClientPermissions(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True

        if request.method in owner_methods:
            if request.user == obj.sales_contact:
                return True

            elif request.user.role == "Manager":
                return True


class ContractPermissions(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):

        if request.method == "GET":
            return True

        elif request.method in owner_methods:
            if request.user == obj.sales_contact:
                return True

            elif request.user.role == "Manager":
                return True


class EventPermissions(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        client = Client.objects.get(id=str(obj.client.id))

        if request.method == "GET":
            return True

        elif request.method in owner_methods:
            if (
                request.user.id == obj.support_contact.id
                or request.user.id == client.sales_contact.id
            ):
                return True

            elif request.user.role == "Manager":
                return True
