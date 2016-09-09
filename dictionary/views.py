

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from language.models import Language
from word.models import Word


def dict_view(request, origin='ENG', target='BAR', word=''):
    if request.method == 'POST':
        origin = request.POST['origin']
        target = request.POST['target']
        word = request.POST['word']
        return redirect('/dict/{}{}/{}'.format(origin, target, word))
    else:
        return dict_view_after_search(request, origin, target, word)


def dict_view_after_search(request, origin, target, word):
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
