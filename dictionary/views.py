

from django.views import generic
from django.shortcuts import render, redirect

from .models import Word, Language


def dict_view(request, origin='ENG', target='BAR', word=''):
    if request.method == 'POST':
        origin = request.POST['origin']
        target = request.POST['target']
        word = request.POST['word']
        return redirect('/dict/{}{}/{}'.format(origin, target, word))
    else:
        words = Word.objects.filter(word__regex=word, language__name=origin)
        kwargs = {
            'words': words,
            'origin_word': word,
            'languages': Language.objects,
            'origin': origin,
            'target': target,
        }
        return render(request, 'dictionary/main.html', kwargs)
