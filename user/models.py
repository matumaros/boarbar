

from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from language.models import Language


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    reputation = models.IntegerField(default=0)
    place = models.CharField(max_length=150)
    max_suggest_words_per_day = models.IntegerField(default=10)

    def __str__(self):
        return self.user.username

    @property
    def has_used_suggested_words_limit(self):
        used = self.submitted_words.filter(
            creation_date__gte=datetime.now()-timedelta(days=1)
        ).count()
        return used >= self.max_suggest_words_per_day

class UserLanguage(models.Model):
    PROF = (
        ('beginner', 'beginner'),
        ('novice', 'novice'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
        ('fluent', 'fluent'),
        ('native', 'native'),
    )
    user = models.ForeignKey(Profile, related_name='languages')
    language = models.ForeignKey(Language, related_name='user_languages')
    proficiency = models.CharField(
        max_length=25, default='beginner', choices=PROF
    )

    def __str__(self):
        return ' - '.join([self.language.name, self.proficiency])
