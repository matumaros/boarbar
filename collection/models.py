

import re

from django.db import models
from simple_history.models import HistoricalRecords

from user.models import Profile
from word.models import Word


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
    PROC_MODS = {
        'title': lambda s: s.title(),
    }

    author = models.CharField(max_length=100)
    reporter = models.ForeignKey(Profile, related_name='collection_items')
    title = models.CharField(max_length=150)
    text = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=TYPES)
    history = HistoricalRecords()

    def __str__(self):
        return ' '.join([self.title, 'by', self.author])

    @property
    def processed_text(self):
        def repl(match):
            id = int(match.group(1))
            mods = match.group(2).split(' ')
            word = Word.objects.filter(id=id)
            if word.exists():
                word = word.first()
                word = f'''<a href="/word/{word.id}">{word.word}</a>'''
                for mod in mods:
                    word = self.PROC_MODS.get(mod, lambda s: s)(word)
            else:
                word = f'[No word match for id: {id}]'
            return word
        sub = r'\[(\d+):?([\w ]*)\]'
        return re.sub(sub, repl, self.text)
