

from django.shortcuts import render, redirect

from .models import Word, Description
from language.models import Language


def word_view(request, word_id):
    kwargs = {
        'word': Word.objects.get(pk=word_id),
    }
    return render(request, 'word/display.html', kwargs)


def suggest_view(request):
    if request.method == 'POST':
        word = request.POST['word']
        description_short = request.POST['desc_short']
        description_long = request.POST['desc_long']

        language = Language.objects.get(name='BAR')
        desc = Description.objects.create(
            short=description_short,
            extended=description_long,
            language=language,
        )
        word = Word.objects.create(
            word=word,
            status='SUG',
            version='boarV1',
        )
        word.desc.add(desc)
        return redirect('/word/{}'.format(word.id))
    else:
        return render(request, 'word/suggest.html')
