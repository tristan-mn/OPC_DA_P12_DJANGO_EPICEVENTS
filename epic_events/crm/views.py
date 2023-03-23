import logging

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from crm.models import Client, Contract, Event
from crm.serializers import ClientListSerializer, ClientDetailSerializer
from crm.serializers import ContractListSerializer, ContractDetailSerializer
from crm.serializers import EventListSerializer, EventDetailSerializer
from authentication.permissions import ClientPermissions, ContractPermissions, EventPermissions
# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler("crm.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class ClientViewSet(ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    details_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'email']
    
    def get_queryset(self):
        try:
            queryset = Client.objects.all()
        except:
            logger.exception('something went wrong\n')
        else:
            return queryset


    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception('something went wrong\n')
        else:
            return super().get_serializer_class()



class ContractViewSet(ModelViewSet):

    serializer_class = ContractListSerializer
    details_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'date_created', 'amount']

    def get_queryset(self):
        try:
            queryset = Contract.objects.all()
            client_last_name = self.request.query_params.get('last_name')
            if client_last_name is not None:
                queryset = queryset.filter(client__last_name=client_last_name)
        except:
            logger.exception('something went wrong\n')
        else:
            return queryset

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception('something went wrong\n')
        else:
            return super().get_serializer_class()



class EventViewSet(ModelViewSet):

    serializer_class = EventListSerializer
    details_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, EventPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['client', 'event_date']

    def get_queryset(self):
        try:
            queryset = Event.objects.all()
            client_last_name = self.request.query_params.get('last_name')
            client_email = self.request.query_params.get('email')

            if client_last_name is not None:
                queryset = queryset.filter(client__last_name=client_last_name)

            elif client_email is not None:
                queryset = queryset.filter(client__email=client_email)
        except:
            logger.exception('something went wrong\n')
        else:
            return queryset

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception('something went wrong\n')
        else:
            return super().get_serializer_class()