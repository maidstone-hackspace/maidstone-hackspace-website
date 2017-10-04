from django.db import models
import datetime


class RegisteredUserManager(models.Manager):

    def is_registered(self, name):
        if name is None:
            return False

        today = datetime.date.today() - datetime.timedelta(days=1)
        return super(RegisteredUserManager, self).get_queryset().filter(name=name, created_at__gt=today).exists()
