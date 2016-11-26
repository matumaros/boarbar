

from django.db import models

from user.models import Profile


class Comment(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(Profile)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
