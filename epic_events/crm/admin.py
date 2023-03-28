from django.contrib import admin

from crm.models import Contract, Event, Client

# Register your models here.

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
