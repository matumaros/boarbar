

from django.contrib.auth.models import User
from django.db import models

from language.models import Language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.user.username


class UserLanguage(models.Model):
    user = models.ForeignKey(Profile, related_name='languages')
    language = models.ForeignKey(Language, related_name='user_languages')
    proficiency = models.PositiveIntegerField()

    def __str__(self):
        return self.language.name
