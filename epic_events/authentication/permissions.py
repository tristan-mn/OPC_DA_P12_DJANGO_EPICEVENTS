from rest_framework.permissions import BasePermission, SAFE_METHODS
from crm.models import Event, Client, Contract

class ClientPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Supports'):
            return request.method in SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):
        event = Event.objects.filter(support_staff=request.user, client=obj)
        if request.user.groups.filter(name='Sellers'):
            if request.user == obj.sales_contact:
                return True
        elif request.user.groups.filter(name='Supports'):
            if event:
                return request.method in SAFE_METHODS
        elif request.user.groups.filter(name='Managers'):
            return True
        return False


class ContractPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            client = Client.objects.get(id=int(request.data['client']))
            if client.sales_contact != request.user:
                return False
        if request.user.role == "Support":
            return request.method in SAFE_METHODS
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
        if request.method == 'POST':
            client = Client.objects.get(id=int(request.data['client']))
            if request.user.role == "Support":
                return request.method in SAFE_METHODS
            if client.sales_contact != request.user:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        client = Client.objects.get(id=str(obj.client.id))
        if request.user.id == obj.support_contact.id or request.user.id == client.sales_contact.id:
            return True
        elif request.user.role == "Manager":
            return True
        return False