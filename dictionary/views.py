

import logging
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from language.models import Language
from user.models import Profile, UserLanguage
from word.models import Word, Tag
from word.views import get_highest_language_proficiency
from word.views import SuggestView

logger = logging.getLogger(__name__)


class DictView(SuggestView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get', 'post']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        word = context['word'] or ''
        sourcelang = context['sourcelang'] or 'ENG'
        search = '.*(^| +){word}($| +).*'.format(word=word)
        words = Word.objects.filter(
            word__iregex=search,
            version__language__name=sourcelang,
        ).all()
        context.update({
            'languages': Language.objects.all(),
            'sourcelang': sourcelang,
            'targetlang': context['targetlang'] or 'BAR',
            'words': words,
            'word': word,
        })
        context["tags"] = Tag.objects.all()
        context["synonyms"] = Word.objects.all()
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
