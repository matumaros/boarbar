from django import forms

from collection.models import Collection


class CollectionForm(forms.Form):

    class Meta:
        model = Collection
        fields = ('title', 'author', 'text', 'type', 'reporter')