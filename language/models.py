

from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    default_variant = models.CharField(
        max_length=5,
        blank=True,
        help_text="Variant of the language such as 'bv_DA' for Danube Bavarian"
    )

    def __str__(self):
        return self.name
