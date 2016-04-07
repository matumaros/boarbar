

from django.contrib.auth.models import User
from django.db import models

from dictionary.models import Language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class UserLanguage(models.Model):
    user = models.ForeignKey(Profile)
    language = models.OneToOneField(Language)
    proficiency = models.PositiveIntegerField()
