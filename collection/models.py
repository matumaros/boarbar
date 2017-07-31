

from django.db import models

from simple_history.models import HistoricalRecords

from user.models import Profile


class Collection(models.Model):
    """A collection of words and sentences"""
    TYPES = (
        ('song_lyrics', 'liad'),
        ('tongue_twister', 'zunga breha'),
        ('saying', 'šbruh'),
        ('poem', 'gedihd'),
        ('story', 'gšihd'),
        ('help', 'huif'),
    )

    author = models.CharField(max_length=100)
    reporter = models.ForeignKey(Profile, related_name='collection_items')
    title = models.CharField(max_length=150)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=TYPES)
    history = HistoricalRecords()

    def __str__(self):
        return ' '.join([self.title, 'by', self.author])
