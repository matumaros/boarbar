

import re

from django.db import models
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

from user.models import Profile
from word.models import Word


class Collection(models.Model):
    """A collection of words and sentences"""
    TYPES = (
        ('song_lyrics', _('song_lyrics')),
        ('tongue_twister', _('tongue_twister')),
        ('saying', _('saying')),
        ('poem', _('poem')),
        ('story', _('story')),
        ('help', _('help')),
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
    def processed_text(self, format_):
        def repl(match):
            id = int(match.group(1))
            mods = match.group(2).split(' ')
            word = Word.objects.filter(id=id)
            if word.exists():
                word = word.first().format(id=word.id, word=word.word)
                for mod in mods:
                    word = self.PROC_MODS.get(mod, lambda s: s)(word)
            else:
                word = f'[No word match for id: {id}]'
            return word
        sub = r'\[(\d+):?([\w ]*)\]'
        return re.sub(sub, repl, self.text)
