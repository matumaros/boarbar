

from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50)


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Language(models.Model):
    name = models.CharField(max_length=50)


class Dialect(models.Model):
    name = models.CharField(max_length=50)
    language = models.ForeignKey(Language)


class Word(models.Model):
    word = models.CharField(max_length=50)
    language = models.ForeignKey(Language)
    dialects = models.ManyToManyField(Dialect)
    tags = models.ManyToManyField(Tag, blank=True)
    standard = models.BooleanField()
    synonyms = models.ManyToManyField(
        'self', related_name='synonyms', blank=True
    )
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
