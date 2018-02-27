from django import forms

from word.models import Word


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['audio']
