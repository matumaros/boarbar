

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from language.models import Language
from word.models import Word


def dict_view(request, sourcelang='ENG', word=''):
    if request.method == 'POST':
        sourcelang = request.POST['sourcelang']
        word = request.POST['word']
        trans = request.POST['trans']
        return redirect('/dict/{}/{}'.format(sourcelang, word))
    else:
        return dict_view_after_search(request, sourcelang, word)


def dict_view_after_search(request, sourcelang, word):
    search = '.*(^| +){word}($| +).*'.format(word=word)
    words = Word.objects.filter(word__iregex=search, language__name=origin)
    kwargs = {
        'words': words,
        'origin_word': word,
        'languages': Language.objects,
        'origin': origin,
        'target': target,
    }
    return render(request, 'dictionary/main.html', kwargs)
