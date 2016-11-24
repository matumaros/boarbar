

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from language.models import Language
from word.models import Word, Translation


class DictView(TemplateView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set only needed things, because origin word is empty and
        # collection empty too (don't search anything)
        context.update({
            'languages': Language.objects.all(),
            'target': 'ENG',
        })
        return context

    def post(self, request, *args, **kwargs):
        sourcelang = request.POST.get('sourcelang', 'eng').upper()
        word = request.POST.get('word', '')

        kwargs = {'sourcelang': sourcelang, 'word': word}
        url = reverse_lazy('dict_view_after_search', kwargs=kwargs)
        return HttpResponseRedirect(url)


class DictAfterSearchView(TemplateView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sourcelang = kwargs.get('sourcelang', 'eng').upper()
        word = kwargs.get('word', '')

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

        context.update({
            'words': collection,
            'languages': Language.objects.all(),
            'origin': word,
            'target': sourcelang,
        })
        return context
