

from django.shortcuts import render

from .models import BavarianWord


def word_view(request, word_id):
    kwargs = {
        'word': BavarianWord.objects.get(pk=word_id)
    }
    return render(request, 'word/main.html', kwargs)
