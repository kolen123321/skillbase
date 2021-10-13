from django.db import models
from accounts.models import DiscordUser
# Create your models here.
import datetime, jwt, time
from skillbase_api import settings

from rest_framework.authtoken.models import Token

from asgiref.sync import sync_to_async

class Mod(models.Model):
    name = models.CharField(max_length=128)
    code = models.FileField(upload_to="mods_files/")

    def __str__(self):
        return self.name

class HaveMod(models.Model):
    user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)
    mods = models.ManyToManyField(Mod, blank=True)

    def __str__(self):
        return f"{self.user.discord_id}"

def get_expire():
    return datetime.datetime.now() + datetime.timedelta(minutes = 1)
