from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from language.models import Language
from word.models import BavarianWord, ForeignWord


class DictView(TemplateView):
    template_name = 'dictionary/main.html'
    http_methods_name = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: Rewrite to use a FormView with SearchForm
        languages = Language.objects.all()
        context.update({
            'languages': languages,
            'target': 'ENG'
        })

        return context

    def post(self, request, *args, **kwargs):
        source_lang = request.POST.get('sourcelang', 'ENG')
        word = request.POST.get('word', '')

        kwargs = {'sourcelang': source_lang, 'word': word}
        url = reverse('dictionary:dict_search_view', kwargs=kwargs)
        return HttpResponseRedirect(url)

class DictSearhView(TemplateView):
    template_name = 'dictionary/main.html'
    http_methods_name = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        word = kwargs.get('word')
        source_lang = kwargs.get('sourcelang')

        search = '.*(^| +){word}($| +).*'.format(word=word)
        words = BavarianWord.objects.filter(
            word__iregex=search
        )
        trans = ForeignWord.objects.filter(
            word__iregex=search, language__name=source_lang
        )
        languages = Language.objects.all()

        context.update({
            'words': words,
            'trans': trans,
            'languages': languages,
            'origin': word,
            'target': source_lang
        })

        return context
