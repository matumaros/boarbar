

from django.db import models

from simple_history.models import HistoricalRecords

from share.models import Comment as BaseComment


class ProposalTopic(models.Model):
    STATUS = (
        ('open', 'open'),
        ('closed', 'closed'),  # not possible to add proposals
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Proposal(models.Model):
    STATUS = (
        ('suggested', 'suggested'),  # editable by the creator,
                                     # possibility to add comments
        ('proposed', 'proposed'),  # not editable anymore, people can vote
        ('accepted', 'accepted'),
        ('declined', 'declined'),
    )

    title = models.CharField(max_length=50)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    creation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS)
    topic = models.ForeignKey(ProposalTopic)
    history = HistoricalRecords()

    def __str__(self):
        return self.title


class Comment(BaseComment):
    history = HistoricalRecords()
