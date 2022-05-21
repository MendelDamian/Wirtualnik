import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    """
    Custom user model.
    """

    # Join date.
    date_joined = models.DateTimeField(_("Join date"), auto_now_add=True, db_index=True)
    # UUID.
    uuid = models.UUIDField(_("UUID"), default=uuid.uuid4, editable=False, unique=True, db_index=True)

    def __str__(self):
        return self.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
