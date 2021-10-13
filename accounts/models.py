from django.db import models
import datetime

from requests.api import delete
import random
import string, jwt, time
from skillbase_api import settings

# Create your models here.
class DiscordUser(models.Model):
    discord_id = models.CharField(max_length=128)
    username = models.CharField(max_length=256, null=True, blank=True)

    license_id = models.CharField(max_length=256, default="")

    def __str__(self):
        return self.discord_id

    @property
    def token(self, request, days=30):
        return jwt.encode({
            'id': self.id,
            'exp': time.time() + days * 24 * 60 * 60,
            'ip': request.META['REMOTE_ADDR']
        }, key=settings.SECRET_KEY, algorithm='HS256')

def get_expire():
    return datetime.datetime.now() + datetime.timedelta(minutes = 1)

class SecretCode(models.Model):
    user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE, null=True)
    expire = models.DateTimeField(default=get_expire)
    code = models.CharField(max_length=128, default=''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(12)]), unique=True)
