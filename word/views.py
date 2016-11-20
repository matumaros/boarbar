

from django.shortcuts import render

from .models import BavarianWord
from language.models import Language


def word_view(request, word_id):
    kwargs = {
        'languages': Language.objects,
        'word': BavarianWord.objects.get(pk=word_id),
    }
    return render(request, 'word/display.html', kwargs)
