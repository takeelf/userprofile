from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


def upload_to_background(instance, filename):
    return 'uploaded/{0}/user/bg/{1}'.format(instance.user.username, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    real_name = models.CharField(max_length=100, null=True, blank=True)
    is_authentication = models.BooleanField(default=False)
    thumbnail_file = models.ImageField(null=True, blank=True, upload_to=upload_to_background)
