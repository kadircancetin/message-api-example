from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Block
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        blocked = get_object_or_404(User.objects, id=kwargs["user_id"])
        Block.objects.get_or_create(blocker=self.request.user, blocked=blocked)
        return Response(data={}, status=status.HTTP_201_CREATED)


class UnBlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        blocked = get_object_or_404(User.objects, id=kwargs["user_id"])
        Block.objects.filter(blocker=self.request.user, blocked=blocked).delete()
        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
