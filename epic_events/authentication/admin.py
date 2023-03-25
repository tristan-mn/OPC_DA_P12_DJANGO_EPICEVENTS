from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from authentication.models import CustomUser
from authentication.forms import CustomUserCreationForm
from django.contrib.auth.models import Group, Permission


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    list_display = ('id','username', 'first_name', 'last_name', 'email', 'role', 'last_login')

    fieldsets = (*UserAdmin.fieldsets, ('User role', {'fields': ('role', )}))

    add_fieldsets = (*UserAdmin.add_fieldsets, ('Staff', {'fields': ('first_name', 'last_name', 'role')}))



def create_managers_group():
    managers_permissions = Permission.objects.all()
    managers_group = Group.objects.create(name='Managers')
    managers_group.permissions.set(managers_permissions)


def create_sellers_group():
    sellers_permissions = []
    all_permissions = Permission.objects.all()
    for permission in all_permissions:
        if "client" in permission.codename:
            sellers_permissions.append(permission)
        elif "contract" in permission.codename:
            sellers_permissions.append(permission)


    sellers_group = Group.objects.create(name='Sellers')
    sellers_group.permissions.set(sellers_permissions)


def create_supports_group():
    supports_permissions = []
    all_permissions = Permission.objects.all()
    for permission in all_permissions:
        if "event" in permission.codename:
            supports_permissions.append(permission)
        elif "client" in permission.codename:
            supports_permissions.append(permission)

    supports_group = Group.objects.create(name='Supports')
    supports_group.permissions.set(supports_permissions)

    
if len(Group.objects.all()) == 0:
    create_managers_group()
    create_sellers_group()
    create_supports_group()


admin.site.register(CustomUser, CustomUserAdmin)