import datetime

from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


# Create your models here.


class PanelUser(AbstractUser):
    email = models.EmailField(unique=True)


class Dzial(models.Model):
    dzial = models.CharField(max_length=50)

    def __str__(self):
        return self.dzial


class Server(models.Model):
    serwer = models.CharField(max_length=50)

    def __str__(self):
        return self.serwer


class Rangs(models.Model):
    ranga = models.CharField(max_length=50)

    def __str__(self):
        return self.ranga


class UsersProfile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(PanelUser, related_name="profile", on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    ranga = models.ForeignKey(Rangs, related_name="rangs", on_delete=models.CASCADE, null=True)
    dzial = models.ForeignKey(Dzial, related_name="dziall", on_delete=models.CASCADE, null=True)
    serwer = models.ForeignKey(Server, related_name="server", on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        permissions = (('zarzad', 'ma uprawnienia zarzadu'),)

    def __str__(self):
        return "Profile: %s" % self.user.username

    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.25)
