

from django.views import generic
from django.shortcuts import render

from .models import Word, Language


def dict_view(request, origin='ENG', target='BAR', word=''):
    words = Word.objects.filter(word__regex=word, language__name=origin)
    kwargs = {
        'words': words,
        'languages': Language.objects,
        'origin': origin,
        'target': target,
    }
    return render(request, 'dictionary/main.html', kwargs)
