from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    value = models.BigIntegerField(default=0)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


class SocialAuthUser(models.Model):
    email = models.EmailField(unique=True)
    provider = models.CharField(max_length=20)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


@receiver(
    signal=models.signals.post_save,
    sender=User,
    dispatch_uid='api.user.create_auth_token'
)
def create_auth_token(sender, instance, created, **kwargs):
    if (created):
        token = Token.objects.create(user=instance)
        token.save()