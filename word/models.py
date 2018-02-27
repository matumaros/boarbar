

from django.db import models

from simple_history.models import HistoricalRecords

from language.models import Language
from user.models import Profile
from word.validators import FileValidator


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Description(models.Model):
    short = models.CharField(max_length=150)
    extended = models.TextField(blank=True)
    language = models.ForeignKey(Language, related_name='descriptions',
                                 on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.short}: {self.extended}"


class WordVersion(models.Model):
    """A word version is the orthography version that is used for a word and
    also different writing systems. For example Russian can be written in
    Cyrillic and it can also be written in Latin script. Cyrillic can be the
    primary WordVersion of Russian and Latin would be a secondary WordVersion. """

    name = models.CharField(max_length=50, unique=True)
    link = models.CharField(max_length=150, default='')
    creation_date = models.DateField(auto_now_add=True)
    language = models.ForeignKey(Language, related_name='versions',
                                 on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

def my_file_validator(value):
    print("W"*10, value)

class AbstractWord(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),  # Suggested by a user
        ('EVL', 'Evaluated'),  # Evaluated by the community
        ('CFR', 'Confirmed'),  # Confirmed by moderators
        ('RMV', 'Removed'),   # Removed
    )

    word = models.CharField(max_length=150)
    ipa = models.CharField(default='', max_length=150, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    desc = models.ManyToManyField(Description, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    # TODO: file upload validator is not running. needs fixing
    audio = models.FileField(
        validators=[FileValidator(max_size=24 * 1024 * 1024)],
        upload_to="audio/%Y/%m/%d",
        blank=True,
        null=True)
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    version = models.ForeignKey(WordVersion, related_name='words',
                                on_delete=models.SET_NULL, null=True)
    wiktionary_link = models.CharField(max_length=150, blank=True)
    submitter = models.ForeignKey(Profile, related_name='submitted_words',
                                  on_delete=models.SET_NULL, null=True)

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
    word = models.ForeignKey(Word, blank=True, related_name='locations',
                             on_delete=models.CASCADE)
    place = models.CharField(max_length=150)
    submitter = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.place
