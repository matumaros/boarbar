

from django.db import models

from user.models import Profile


class CollectionItem(models.Model):
    KINDS = (
        ('song', 'liad'),
        ('tongue_twister', 'zunga breha'),
        ('saying', 'šbruh'),
        ('poem', 'gedihd'),
    )

    author = models.CharField(max_length=100)
    reporter = models.ForeignKey(Profile)
    title = models.CharField(max_length=150)
    text = models.TextField()
    kind = models.CharField(max_length=50, choices=KINDS)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
