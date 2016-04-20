

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from .models import Word, Language


def dict_view(request, origin='ENG', target='BAR', word=''):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details supplied.')
            return dict_view_after_search(request, origin, target, word)
        else:
            origin = request.POST['origin']
            target = request.POST['target']
            word = request.POST['word']
            return redirect('/dict/{}{}/{}'.format(origin, target, word))
    else:
        return dict_view_after_search(request, origin, target, word)


def dict_view_after_search(request, origin, target, word):
    words = Word.objects.filter(word__regex=word, language__name=origin)
    kwargs = {
        'words': words,
        'origin_word': word,
        'languages': Language.objects,
        'origin': origin,
        'target': target,
    }
    return render(request, 'dictionary/main.html', kwargs)
