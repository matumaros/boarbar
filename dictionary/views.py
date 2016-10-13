

from django.shortcuts import render, redirect

from language.models import Language
from word.models import Word


def dict_view(request, sourcelang='ENG', word=''):
    if request.method == 'POST':
        sourcelang = request.POST['sourcelang']
        word = request.POST['word']
        return redirect('/dict/{}/{}'.format(sourcelang, word))
    else:
        return dict_view_after_search(request, sourcelang, word)


def dict_view_after_search(request, sourcelang, word):
    search = '.*(^| +){word}($| +).*'.format(word=word)
    words = Word.objects.filter(word__iregex=search, language__name='BAR')
    trans = Word.objects.filter(word__iregex=search, language__name=sourcelang)

    kwargs = {
        'words': words,
        'trans': trans,
        'languages': Language.objects,
        'origin': word,
        'target': sourcelang,
    }
    return render(request, 'dictionary/main.html', kwargs)
