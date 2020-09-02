from django.db import models


class Log(models.Model):
    class Types(models.TextChoices):
        SIGN_UP = "SIGIN_UP"
        BLOCK = "BLOCK"
        UN_BLOCK = "UN_BLOCK"
        MESSAGE_SEND = "MESSAGE_SEND"
        VALID_LOGIN = "LOGIN"
        INVALID_LOGIN = "INVALID_LOGIN"

    creation_datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=64, choices=Types.choices)

    user = models.ForeignKey(
        "auth.User",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="logs",
    )
    affected_user = models.ForeignKey(
        "auth.User",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="affected_logs",
    )

    data = models.TextField(blank=True, null=True)
