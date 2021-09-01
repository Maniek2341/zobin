import datetime

from django.conf.global_settings import MEDIA_URL
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin, User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


# Create your models here.


class Server(models.Model):
    serwer = models.CharField(max_length=50)

    def __str__(self):
        return self.serwer


class Rangs(models.Model):
    ranga = models.CharField(max_length=50)

    def __str__(self):
        return self.ranga


class PanelUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(_('password'), max_length=128)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    DZIAL_CZLONEK = 1
    DZIAL_DYREKCJA = 2
    DZIAL_ZARZAD = 3
    DZIAL_CHOICES = [
        (DZIAL_CZLONEK, _("Członek")),
        (DZIAL_DYREKCJA, _("Dyrekcja")),
        (DZIAL_ZARZAD, _("Zarząd")),
    ]

    birthday = models.DateField(blank=True, null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, blank=True, default=GENDER_MALE)

    ranga = models.ForeignKey(Rangs, related_name="rang", on_delete=models.CASCADE, blank=True, null=True)
    dzial = models.PositiveSmallIntegerField(choices=DZIAL_CHOICES, blank=True, default=DZIAL_CZLONEK)
    serwer = models.ForeignKey(Server, related_name="server", blank=True, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = _('Użytkownik')
        verbose_name_plural = _('Użytkownicy')

    def __str__(self):
        return "Profile: %s" % self.username

    def age(self):
        return int((datetime.date.today() - self.birthday).days / 365.25)