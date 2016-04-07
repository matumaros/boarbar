

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Language(models.Model):
    name = models.CharField(max_length=50)


class Word(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),
        ('CFR', 'Confirmed'),
        ('RMV', 'Removed'),
    )

    word = models.CharField(max_length=50)
    language = models.ForeignKey(Language)
    tags = models.ManyToManyField(Tag, blank=True)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()
    standard = models.BooleanField()
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    synonyms = models.ManyToManyField(
        'self', related_name='synonyms', blank=True
    )
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
