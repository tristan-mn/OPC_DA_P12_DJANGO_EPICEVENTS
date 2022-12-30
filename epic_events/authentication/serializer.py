from rest_framework.serializers import ModelSerializer
from authentication.models import CustomUser

class UserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'role', 'date_joined']