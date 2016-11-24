

from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.shortcuts import render, redirect

from .models import Word, Description
from language.models import Language


class WordView(DetailView):
    template_name = 'word/display.html'
    http_method_names = ['get']
    model = Word


class SuggestView(TemplateView):
    template_name = 'word/suggest.html'
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        word = request.POST.get('word')
        description_short = request.POST.get('desc_short')
        description_long = request.POST.get('desc_long')

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

        url = reverse_lazy('word_view', kwargs={'pk': word.id})
        return HttpResponseRedirect(url)
