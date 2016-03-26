

from django.views import generic
from django.shortcuts import render

from .models import Word


def dict_view(request, origin='ENG', trans='BAR', word=''):
    words = Word.objects.filter(word__regex=word, language__name=origin)
    kwargs = {
        'words': words,
        'trans': trans
    }
    return render(request, 'dictionary/index.html', kwargs)
