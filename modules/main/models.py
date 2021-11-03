from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from modules.users.models import PanelUser


class Messages(models.Model):
    user = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='tworca')
    mess = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _('Ogłoszenie')
        verbose_name_plural = _('Ogłoszenia')

    def __str__(self):
        return "Wiadomość od: %s o treści: %s" % (self.user.username, self.mess)