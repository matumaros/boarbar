

from django.db import models

from share.models import Profile
from dictionary.models import Word


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
    suggestion = models.ForeignKey(Suggestion)
