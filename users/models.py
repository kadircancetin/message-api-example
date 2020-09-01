from django.db import models


class Block(models.Model):
    blocker = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="blocked_users")
    blocked = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="blocker_users")

    # TODO: db constraint blocker is not same the blocked
