from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404
from logs.models import Log
from message.models import Message
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
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


class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def create_valid_login_log(self, user):
        Log(user=user, type=Log.Types.VALID_LOGIN).save()

    def create_invalid_login_log(self, serializer):
        username = self.request.data['username']
        if username:
            try:
                Log(
                    type=Log.Types.INVALID_LOGIN,
                    user=User.objects.get(username=username),
                ).save()
            except User.DoesNotExist:
                Log(type=Log.Types.INVALID_LOGIN).save()
        else:
            Log(type=Log.Types.INVALID_LOGIN).save()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if not serializer.is_valid():
            self.create_invalid_login_log(serializer)
            serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        with transaction.atomic():
            token, created = Token.objects.get_or_create(user=user)
            self.create_valid_login_log(user)
            return Response({"token": token.key})


class BlockUserView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, *args, **kwargs):
        blocked = get_object_or_404(User.objects, username=kwargs["username"])
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
        blocked = get_object_or_404(User.objects, username=kwargs["username"])
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
