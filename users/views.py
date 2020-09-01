from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
