

from django.db import models


from language.models import Language


def audio_path(instance, filename):
    return 'audio/{}'.format(instance.id)


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AbstractTranslation(models.Model):
    word = models.CharField(max_length=50)
    short_desc = models.CharField(max_length=100)
    desc = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    audio = models.FileField(upload_to=audio_path, blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class AbstractWord(AbstractTranslation):
    WORD_STATUS = (
        ('SUG', 'Suggested'),  # Suggested by a user
        ('EVL', 'Evaluated'),  # Evaluated by the community
        ('CFR', 'Confirmed'),  # Confirmed by moderators
        ('RMV', 'Removed'),   # Removed
    )

    status = models.CharField(max_length=50, choices=WORD_STATUS)
    translations = models.ManyToManyField(
        'Translation', related_name='translations', blank=True
    )
    synonyms = models.ManyToManyField(
        'self', related_name='synonyms', blank=True
    )
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.word


class Word(AbstractWord):
    def save(self):
        super().save()
        h = WordHistory()
        h.old = self
        h.word = self.word
        h.short_desc = self.short_desc
        h.desc = self.desc
        h.upvotes = self.upvotes
        h.downvotes = self.downvotes
        h.creation_date = self.creation_date
        h.status = self.status
        h.audio = self.audio
        h.version = self.version
        h.save()
        h.tags.add(*self.tags.all())
        h.translations.add(*self.translations.all())
        h.synonyms.add(*self.synonyms.all())
        h.save()


class Translation(AbstractTranslation):
    pass


class WordHistory(AbstractWord):
    old = models.ForeignKey(Word)

    class Meta:
        ordering = ['-pk']
