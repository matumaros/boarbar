

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from language.models import Language
from word.models import Word


class DictView(TemplateView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        word = context['word'] or ''
        sourcelang = context['sourcelang'] or 'ENG'
        search = '.*(^| +){word}($| +).*'.format(word=word)
        words = Word.objects.filter(
            word__iregex=search,
            language__name=sourcelang,
        ).all()
        context.update({
            'languages': Language.objects.all(),
            'sourcelang': sourcelang,
            'targetlang': context['targetlang'] or 'BAR',
            'words': words,
            'word': word,
        })
        return context

    def post(self, request, *args, **kwargs):
        sourcelang = request.POST.get('sourcelang') or 'BAR'
        targetlang = request.POST.get('targetlang') or 'BAR'
        word = request.POST.get('word', '')

        kwargs = {
            'sourcelang': sourcelang,
            'targetlang': targetlang,
            'word': word,
        }
        # url = reverse_lazy('dictionary:dict_view', kwargs=kwargs)
        # Fixme: reverse doesn't seem to work for some reason
        return HttpResponseRedirect(f'/dict/{sourcelang}/{targetlang}/{word}')


class DictAfterSearchView(TemplateView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sourcelang = kwargs.get('sourcelang', 'BAR').upper()
        word = kwargs.get('word', '')

        search = '.*(^| +){word}($| +).*'.format(word=word)
        words = Word.objects.filter(
            word__iregex=search
        )
        if sourcelang == 'BAR':
            collection = {
                word.id: {'word': word, 'trans': word.synonyms.all()}
                for word in words if word.synonyms.exists()
            }
        else:
            trans = Translation.objects.filter(
                word__iregex=search, language__name=sourcelang
            )
            collection = {
                word.id: {'word': word, 'trans': word.translations.all()}
                for word in words if word.translations.exists()
            }
            for t in trans:
                wid = t.translation.id
                if wid not in collection:
                    collection[wid] = {'word': t.translation, 'trans': [t]}

        context.update({
            'words': collection,
            'languages': Language.objects.all(),
            'origin': word,
            'target': sourcelang,
        })
        return context
