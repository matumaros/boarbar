

from django.contrib.auth.models import User
from django.db import models

from dictionary.models import Word, Dialect, Language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dialect = models.ForeignKey(Dialect)
    join_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class UserLanguage(models.Model):
    user = models.ForeignKey(Profile)
    language = models.OneToOneField(Language)
    proficiency = models.PositiveIntegerField()


class Discussion(models.Model):
    dtype = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    linked_words = models.ForeignKey(Word)
    pattern = models.CharField(max_length=200)
    final_decision = models.CharField(max_length=500)
    entry_date = models.DateTimeField(auto_now_add=True)
    final_date = models.DateTimeField()
    stage = models.CharField(max_length=50)


class Comment(models.Model):
    description = models.TextField()
    discussion = models.ForeignKey(Discussion)
    positive_votes = models.PositiveIntegerField()
    negative_votes = models.PositiveIntegerField()


class Suggestion(models.Model):
    description = models.CharField(max_length=200)
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(Profile)


class Vote(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile)
