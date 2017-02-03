

import re

from django.db import models

from word.models import Word
from language.models import Language


class Sentence(models.Model):
    text = models.TextField()

    def get(self):
        def repl(match):
            try:
                mod = match.group(1)
                uid = match.group(2)
                word = Word.objects.get(id=uid).word
                if mod == 'c':
                    word = word.title()
                return word
            except TypeError:
                return match.group(0)
        return re.sub(r"{{([c]*)(\d)}}", repl, self.text)

    def __str__(self):
        text = self.get()
        end = 22
        return text[:end] + ('...' if len(text) > end else '')


class Translation(models.Model):
    text = models.TextField()
    sentence = models.ForeignKey(Sentence, related_name='translations')
    language = models.ForeignKey(Language, related_name='foreign_sentences')

    def __str__(self):
        return self.text[:20]
