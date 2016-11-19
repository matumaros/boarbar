

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

    language = models.ForeignKey(Language)
    word = models.CharField(max_length=50)
    desc = models.ManyToManyField(Description, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    version = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class Word(AbstractWord):
    translations = models.ManyToManyField(
        'self', related_name='+',
        blank=True, through='Translation', symmetrical=False,
    )
    history = HistoricalRecords()


class Translation(models.Model):
    bavarian = models.ForeignKey(
        Word, related_name='bavarian', on_delete=models.CASCADE,
    )
    foreign = models.ForeignKey(
        Word, related_name='foreign', on_delete=models.CASCADE,
    )
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    desc = models.ManyToManyField(Description, blank=True)
    creation_date = models.DateField(auto_now_add=True)
