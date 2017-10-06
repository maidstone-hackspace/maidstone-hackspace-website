from django.db import models
import datetime


class RegisteredUserManager(models.Manager):

    def is_registered(self, user):
        today = datetime.date.today()
        return super(RegisteredUserManager, self).get_queryset().filter(user=user, created_at__gte=today).exists()
