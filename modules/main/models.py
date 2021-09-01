from django.db import models
from django.utils import timezone

from modules.users.models import PanelUser


class Messages(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='tworca')
    mess = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Wiadomość od: %s o treści: %s" % (self.user.username, self.mess)