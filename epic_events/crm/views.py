import logging
from datetime import datetime

from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from crm.models import Client, Contract, Event
from crm.serializers import ClientListSerializer, ClientDetailSerializer
from crm.serializers import ContractListSerializer, ContractDetailSerializer
from crm.serializers import EventListSerializer, EventDetailSerializer
from authentication.permissions import (
    ClientPermissions,
    ContractPermissions,
    EventPermissions,
)
from authentication.models import CustomUser
from authentication.serializer import UserSerializer

# Create your views here.

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("crm.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class ClientViewSet(ModelViewSet):

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    details_serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated, ClientPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["last_name", "email"]

    def get_queryset(self):
        try:
            queryset = Client.objects.all()
        except:
            logger.exception("something went wrong\n")
        else:
            return queryset

    def create(self, request, *args, **kwargs):
        serializer = ClientDetailSerializer(data=request.data)
        request.data._mutable = True
        request.data["sales_contact"] = request.user.id
        request.data._mutable = False
        print(request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        try:
            sales_contact = CustomUser.objects.get(id=data["sales_contact"])
            instance.sales_contact = sales_contact
        except KeyError:
            logger.exception("something went wrong\n")

        instance.first_name = data.get("first_name", instance.first_name)
        instance.last_name = data.get("last_name", instance.last_name)
        instance.email = data.get("email", instance.email)
        instance.phone = data.get("phone", instance.phone)
        instance.mobile = data.get("mobile", instance.mobile)
        instance.company_name = data.get("company_name", instance.company_name)
        instance.client_status = data.get("client_status", instance.client_status)

        serializer = ClientDetailSerializer(instance)
        instance.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception("something went wrong\n")
        else:
            return super().get_serializer_class()


class ContractViewSet(ModelViewSet):

    serializer_class = ContractListSerializer
    details_serializer_class = ContractDetailSerializer
    permission_classes = [IsAuthenticated, ContractPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["client", "date_created", "amount"]

    def create(self, request, *args, **kwargs):
        serializer = ContractDetailSerializer(data=request.data)
        request.data._mutable = True
        request.data["sales_contact"] = request.user.id
        request.data._mutable = False
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        try:
            client = Client.objects.get(id=data["client"])
            instance.client = client
        except KeyError:
            logger.exception("something went wrong\n")
        try:
            sales_contact = CustomUser.objects.get(id=data["sales_contact"])
            instance.sales_contact = sales_contact
        except KeyError:
            pass
        instance.amount = data.get("amount", instance.amount)
        instance.status = data.get("status", instance.status)
        instance.payment_due = datetime.now().strftime("%Y-%m-%d")

        serializer = ContractDetailSerializer(instance)
        instance.save()
        return Response(serializer.data)

    def get_queryset(self):
        try:
            queryset = Contract.objects.all()
            client_last_name = self.request.query_params.get("last_name")
            if client_last_name is not None:
                queryset = queryset.filter(client__last_name=client_last_name)
        except:
            logger.exception("something went wrong\n")
        else:
            return queryset

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception("something went wrong\n")
        else:
            return super().get_serializer_class()


class EventViewSet(ModelViewSet):

    serializer_class = EventListSerializer
    details_serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated, EventPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["client", "event_date"]

    def create(self, request, *args, **kwargs):
        serializer = EventDetailSerializer(data=request.data)
        serializer.is_valid()
        if "event_date" in serializer.errors:
            message = "respect the format : YYYY-MM-DD hh:mm"
            return Response(message)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        try:
            client = Client.objects.get(id=data["client"])
            instance.client = client
        except KeyError:
            logger.exception("something went wrong\n")

        try:
            support_contact = CustomUser.objects.get(id=data["support_contact"])
            instance.support_contact = support_contact
        except KeyError:
            logger.exception("something went wrong\n")

        instance.event_status = data.get("event_status", instance.event_status)
        instance.attendees = data.get("attendees", instance.attendees)
        instance.event_date = data.get("event_date", instance.event_date)
        serializer = EventDetailSerializer(instance)
        try:
            instance.save()
        except:
            logger.exception("something went wrong\n")
            return Response("ERROR : respect the format > YYYY-MM-DD hh:mm")
        return Response(serializer.data)

    def get_queryset(self):
        try:
            queryset = Event.objects.all()
            client_last_name = self.request.query_params.get("last_name")
            client_email = self.request.query_params.get("email")

            if client_last_name is not None:
                queryset = queryset.filter(client__last_name=client_last_name)

            elif client_email is not None:
                queryset = queryset.filter(client__email=client_email)
        except:
            logger.exception("something went wrong\n")
        else:
            return queryset

    def get_serializer_class(self):
        try:
            if self.action == "retrieve":
                return self.details_serializer_class
        except:
            logger.exception("something went wrong\n")
        else:
            return super().get_serializer_class()
