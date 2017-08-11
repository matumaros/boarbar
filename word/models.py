

from django.db import models

from simple_history.models import HistoricalRecords

from language.models import Language
from user.models import Profile


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Tag(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Description(models.Model):
    short = models.CharField(max_length=150)
    extended = models.TextField(blank=True)
    language = models.ForeignKey(Language, related_name='descriptions')

    def __str__(self):
        return self.short


class WordVersion(models.Model):
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=150, default='')
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class AbstractWord(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),  # Suggested by a user
        ('EVL', 'Evaluated'),  # Evaluated by the community
        ('CFR', 'Confirmed'),  # Confirmed by moderators
        ('RMV', 'Removed'),   # Removed
    )

    word = models.CharField(max_length=150)
    ipa = models.CharField(default='', max_length=150)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    desc = models.ManyToManyField(Description, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    version = models.ForeignKey(WordVersion, related_name='words')
    wiktionary_link = models.CharField(max_length=150, blank=True)
    language = models.ForeignKey(Language, related_name='words')
    submitter = models.ForeignKey(Profile, related_name='submitted_words')

    class Meta:
        abstract = True

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        if not self.submitter.has_used_suggested_words_limit:
            super().save(*args, **kwargs)
        else:
            raise ValueError("User is over his word suggestion limit")


class Word(AbstractWord):
    synonyms = models.ManyToManyField('self', blank=True)
    history = HistoricalRecords()


class WordLocation(models.Model):
    word = models.ForeignKey(Word, blank=True, related_name='locations')
    place = models.CharField(max_length=150)
    submitter = models.ForeignKey(Profile)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.place
