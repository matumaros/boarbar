

from django.db import models

from simple_history.models import HistoricalRecords

from language.models import Language


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Description(models.Model):
    short = models.CharField(max_length=150)
    extended = models.TextField()
    language = models.ForeignKey(Language)

    def __str__(self):
        return self.short


class AbstractWord(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),  # Suggested by a user
        ('EVL', 'Evaluated'),  # Evaluated by the community
        ('CFR', 'Confirmed'),  # Confirmed by moderators
        ('RMV', 'Removed'),   # Removed
    )

    word = models.CharField(max_length=50)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    desc = models.ManyToManyField(Description, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    version = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class Word(AbstractWord):
    history = HistoricalRecords()


class Translation(models.Model):
    word = models.CharField(max_length=50)
    translation = models.ForeignKey(
        'Word', related_name='translations',
    )
    language = models.ForeignKey(Language)
    tags = models.ManyToManyField(Tag, blank=True)
    wiktionary_link = models.CharField(max_length=150)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    comment = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return '{} ({})'.format(
            self.word,
            self.language.name,
        )
