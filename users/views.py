from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from logs.models import Log
from message.models import Message
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

    @transaction.atomic
    def post(self, *args, **kwargs):
        blocked = get_object_or_404(User.objects, id=kwargs["user_id"])
        _, created = Block.objects.get_or_create(
            blocker=self.request.user, blocked=blocked
        )

        if created:
            Log(
                type=Log.Types.BLOCK, user=self.request.user, affected_user=blocked
            ).save()

        return Response(data={}, status=status.HTTP_201_CREATED)


class UnBlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, *args, **kwargs):
        blocked = get_object_or_404(User.objects, id=kwargs["user_id"])
        delete_count = Block.objects.filter(
            blocker=self.request.user, blocked=blocked
        ).delete()

        if delete_count:
            Log(
                type=Log.Types.UN_BLOCK, user=self.request.user, affected_user=blocked
            ).save()

        Message.objects.filter(
            sender=blocked, reciever=self.request.user, is_blocked=True
        ).update(is_blocked=False)

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)
