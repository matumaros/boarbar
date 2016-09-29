

from django.shortcuts import render

from .models import Word


def word_view(request, word_id):
    kwargs = {
        'word': Word.objects.get(pk=word_id)
    }
    return render(request, 'word/main.html', kwargs)
