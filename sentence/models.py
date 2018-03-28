

import re

from django.db import models

from share.validators import FileValidator
from word.models import Word
from language.models import Language


class Sentence(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),  # Suggested by a user
        ('EVL', 'Evaluated'),  # Evaluated by the community
        ('CFR', 'Confirmed'),  # Confirmed by moderators
        ('RMV', 'Removed'),   # Removed
    )

    text = models.TextField()
    status = models.CharField(max_length=50, choices=WORD_STATUS, default='SUG')
    audio = models.FileField(
        validators=[FileValidator(max_size=24 * 1024 * 1024)],
        upload_to="audio/%Y/%m/%d",
        blank=True,
        null=True
    )
    place = models.CharField(max_length=150)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        text = self.html
        end = 22
        return text[:end] + ('...' if len(text) > end else '')

    @property
    def html(self):
        def repl(match):
            try:
                mods = (match.group(1) or '').split(' ')
                uid = match.group(2)
                word = Word.objects.get(id=uid).word
                for mod in mods:
                    if mod == 'capital':
                        word = word.title()
                html = f"""<a class=word href="{{% url 'word:word_view' {uid} %}}">{word}</a>"""
                return html
            except TypeError:
                return match.group(0)
        return re.sub(r"{{(capital )*word:([0-9]+)}}", repl, self.text)


class Translation(models.Model):
    text = models.TextField()
    sentence = models.ForeignKey(Sentence, related_name='translations',
                                 on_delete=models.SET_NULL, null=True )
    language = models.ForeignKey(Language, related_name='foreign_sentences',
                                 on_delete=models.SET_NULL, null=True)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text[:20]
