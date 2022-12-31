from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Client, Contract, Event


class ClientListSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['__all__']


class ContractListSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = ['id', 'client', 'date_created', 'amount']


class ContractDetailSerializer(ModelSerializer):
    client_surname = serializers.ReadOnlyField(source='client.surname')
    client_email = serializers.ReadOnlyField(source='client.email')

    class Meta:
        model = Contract
        fields = ['__all__']


class EventListSerializer(ModelSerializer):
    client_surname = serializers.ReadOnlyField(source='client.surname')
    client_email = serializers.ReadOnlyField(source='client.email')

    class Meta:
        model = Event
        fields = ['id', 'client', 'client_surname', 'client_email', 'event_date']


class EventDetailSerializer(ModelSerializer):
    customer_company_name = serializers.ReadOnlyField(source='client.company_name')
    customer_sales_staff = serializers.ReadOnlyField(source='client.sales_contact.id')

    class Meta:
        model = Event
        fields = ['__all__']
