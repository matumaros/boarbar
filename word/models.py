

from django.db import models

from language.models import Language


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AbstractWord(models.Model):
    WORD_STATUS = (
        ('SUG', 'Suggested'),
        ('CFR', 'Confirmed'),
        ('RMV', 'Removed'),
    )

    word = models.CharField(max_length=50)
    language = models.ForeignKey(Language)
    tags = models.ManyToManyField(Tag, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    standard = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=WORD_STATUS)
    synonyms = models.ManyToManyField(
        'self', related_name='synonyms', blank=True
    )
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class Word(AbstractWord):
    def save(self):
        old = super(Word, self).save()

        PostHistory.objects.create(
            old=old,
            word=old.word,
            language=old.language,
            tags=old.tags,
            upvotes=old.upvotes,
            downvotes=old.downvotes,
            creation_date=old.creation_date,
            standard=old.standard,
            status=old.status,
            synonyms=old.synonyms,
            audio=old.audio,
            version=old.version,
        )


class WordHistory(AbstractWord):
    old = ForeignKey(Word)

    class Meta:
        ordering = ['-pk']
