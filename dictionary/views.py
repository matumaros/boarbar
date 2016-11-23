

from django.shortcuts import render, redirect

from language.models import Language
from word.models import Word, Translation


def dict_view(request, sourcelang='ENG', word=''):
    if request.method == 'POST':
        sourcelang = request.POST['sourcelang'].upper()
        word = request.POST['word']
        return redirect('/dict/{}/{}'.format(sourcelang, word))
    else:
        return dict_view_after_search(request, sourcelang, word)


def dict_view_after_search(request, sourcelang, word):
    search = '.*(^| +){word}($| +).*'.format(word=word)
    words = Word.objects.filter(
        word__iregex=search
    )
    if sourcelang == 'BAR':
        collection = {
            word.id: {'word': word, 'trans': word.synonyms.all()}
            for word in words if word.synonyms.all()
        }
    else:
        trans = Translation.objects.filter(
            word__iregex=search, language__name=sourcelang
        )
        collection = {
            word.id: {'word': word, 'trans': word.translations.all()}
            for word in words if word.translations.all()
        }
        for t in trans:
            wid = t.translation.id
            if wid not in collection:
                collection[wid] = {'word': t.translation, 'trans': [t]}
            collection[t.translation.id]['trans']

    kwargs = {
        'words': collection,
        'languages': Language.objects,
        'origin': word,
        'target': sourcelang,
    }
    return render(request, 'dictionary/main.html', kwargs)
