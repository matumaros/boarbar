from django import forms

from word.models import Word, Description, Tag
from user.models import UserLanguage


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['audio']


class EditForm(forms.ModelForm):
    user_languages = forms.ModelChoiceField(queryset=UserLanguage.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'})
                                  )
    word = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    ipa = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    wiktionary_link = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    class Meta:
        model = Word
        fields = ('user_languages', 'word', 'ipa', 'desc', 'tags', 'audio', 'wiktionary_link', 'synonyms')


