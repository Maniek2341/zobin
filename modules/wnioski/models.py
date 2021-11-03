from django.db import models
from django.utils.translation import gettext as _

from modules.users.models import PanelUser


class Pochwaly(models.Model):
    created_by = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='created_by')
    powod = models.CharField(max_length=100)
    dowod = models.TextField(max_length=300)
    komu = models.ForeignKey(PanelUser, on_delete=models.CASCADE, related_name='created_for')
    status = models.CharField(max_length=30, default='Nie zatwierdzone')

    class Meta:
        verbose_name = _('Pochwała')
        verbose_name_plural = _('Pochwały')

    def __str__(self):
        return "Pochwała od:  %s" % self.created_by.username
