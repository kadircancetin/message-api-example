from rest_framework import serializers

from message.models import Message
from users.models import Block


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

    def create(self, validated_data):
        sender = self.context["request"].user
        reciever = self.context["other_user"]

        validated_data["sender"] = sender
        validated_data["reciever"] = reciever
        if Block.objects.filter(blocker=reciever, blocked=sender).exists():
            validated_data['blocked'] = True

        return super().create(validated_data)
