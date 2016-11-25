

from django.db import models

from simple_history.models import HistoricalRecords


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
