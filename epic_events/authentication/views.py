from rest_framework.generics import ListAPIView, RetrieveAPIView

from  authentication.serializer import UserSerializer
from authentication.models import CustomUser


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer