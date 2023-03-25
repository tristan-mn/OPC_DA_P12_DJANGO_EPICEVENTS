from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Client, Contract, Event
from authentication.models import CustomUser

class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role']


class ClientListSerializer(ModelSerializer):

    sales_contact = UserSerializer()

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'company_name','email', 'sales_contact']


class ClientDetailSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class ContractListSerializer(ModelSerializer):

    client = ClientDetailSerializer()

    class Meta:
        model = Contract
        fields = ['id', 'client', 'date_created', 'amount']


class ContractDetailSerializer(ModelSerializer):

    class Meta:
        model = Contract
        fields = '__all__'


class EventListSerializer(ModelSerializer):

    client = ClientDetailSerializer()
    # support_contact = UserSerializer()
    # event_contract = ContractListSerializer()

    class Meta:
        model = Event
        fields = ['id', 'client', 'event_status']


class EventDetailSerializer(ModelSerializer):


    class Meta:
        model = Event
        fields = '__all__'
