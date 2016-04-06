

from django.contrib.auth.models import User
from django.db import models

from dictionary.models import Dialect, Language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dialect = models.ForeignKey(Dialect)
    join_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class UserLanguage(models.Model):
    user = models.ForeignKey(Profile)
    language = models.OneToOneField(Language)
    proficiency = models.PositiveIntegerField()
