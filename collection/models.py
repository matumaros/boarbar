

from django.db import models


class CollectionItem(models.Model):
    KINDS = {
        ('song', 'song'),
        ('tongue_twister', 'tongue twister'),
        ('saying', 'saying'),
        ('poem', 'poem'),
    }

    author = models.CharField(max_length=100)
    reporter = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    text = models.TextField()
    kind = models.CharField(max_length=50, choices=KINDS)
    creation_date = models.DateField(auto_now_add=True)
