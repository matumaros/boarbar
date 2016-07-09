

from django.db import models


class CollectionItem(models.Model):
    author = models.CharField(max_length=100)
    reporter = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
