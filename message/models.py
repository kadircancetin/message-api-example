from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="sended_messages"
    )
    reciever = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE, related_name="recieved_messages"
    )
    content = models.TextField()
    is_blocked = models.BooleanField(default=False)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    read_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.sender}->{self.reciever}"

    class Meta:
        ordering = ("-creation_datetime",)
