import logging

from rest_framework.generics import ListAPIView, RetrieveAPIView

from authentication.serializer import UserSerializer
from authentication.models import CustomUser


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")

file_handler = logging.FileHandler("authentication.log")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class UserListView(ListAPIView):
    try:
        queryset = CustomUser.objects.all()
        serializer_class = UserSerializer
    except:
        logger.exception("something went wrong\n")


class UserRetrieveView(RetrieveAPIView):
    try:
        queryset = CustomUser.objects.all()
        serializer_class = UserSerializer
    except:
        logger.exception("something went wrong\n")
