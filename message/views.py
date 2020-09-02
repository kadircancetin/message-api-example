from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from message.models import Message
from message.serializers import MessageSerializer


class MessageListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    @cached_property
    def other_user(self):
        return get_object_or_404(User.objects.all(), **{"id": self.kwargs["user_id"]})

    def get_queryset(self):
        return Message.objects.filter(
            (Q(reciever=self.request.user) & Q(sender=self.other_user))
            | (Q(sender=self.request.user) & Q(reciever=self.other_user))
        ).filter(is_blocked=False)

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context["other_user"] = self.other_user

        return serializer_context
