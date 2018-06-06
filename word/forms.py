from django import forms

from word.models import Word, Description, Tag


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['audio']


class EditForm(forms.ModelForm):
    word = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    ipa = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    desc = forms.ModelChoiceField(queryset=Description.objects.all(),
                                      widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    tags = forms.ModelChoiceField(queryset=Tag.objects.all(),
                                  widget=forms.SelectMultiple(attrs={'class': 'form-control'})
                                  )
    wiktionary_link = forms.CharField(
        max_length=100, required=False, widget=forms.TextInput(attrs={'class': "form-control"})
    )
    synonyms = forms.ModelChoiceField(queryset=Word.objects.all(),
                                  widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Word
        fields = ('word', 'ipa', 'desc', 'tags', 'audio', 'wiktionary_link', 'synonyms')


