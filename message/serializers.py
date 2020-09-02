from django.db import transaction
from logs.models import Log
from rest_framework import serializers
from users.models import Block

from message.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "sender",
            "reciever",
            "content",
            "creation_datetime",
        )
        read_only_fields = (
            "id",
            "sender",
            "reciever",
            "creation_datetime",
        )

    @transaction.atomic
    def create(self, validated_data):
        sender = self.context["request"].user
        reciever = self.context["other_user"]

        validated_data["sender"] = sender
        validated_data["reciever"] = reciever
        if Block.objects.filter(blocker=reciever, blocked=sender).exists():
            validated_data["is_blocked"] = True

        message = super().create(validated_data)

        Log(type=Log.Types.MESSAGE_SEND, user=sender, affected_user=reciever).save()

        return message
