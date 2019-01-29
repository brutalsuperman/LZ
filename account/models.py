from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in


class Profile(AbstractUser):

    last_ip = models.GenericIPAddressField(default='', null=True, blank=True)


def update_ip(sender, user, request, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    user.last_ip = ip
    user.save()


user_logged_in.connect(update_ip)
