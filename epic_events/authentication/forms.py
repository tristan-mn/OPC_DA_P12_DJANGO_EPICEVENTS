from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        managers_group = Group.objects.get(name='Managers')
        sellers_group = Group.objects.get(name='Sellers')
        supports_group = Group.objects.get(name='Supports')
        if user.role == "Manager":
            user.is_superuser = True
            managers_group.user_set.add(user)
        elif user.role == "Seller":
            user.is_staff = True
            user.save()
            sellers_group.user_set.add(user)
        elif user.role == "Support":
            user.is_staff = True
            user.save()
            supports_group.user_set.add(user)
        user.save()
        return user

