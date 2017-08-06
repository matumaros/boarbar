

import re

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from word.models import Word
from language.models import Language


class TransView(TemplateView):
    template_name = 'translator/display.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        def repl(match):
            word = match.group()
            word = Word.objects.filter(
                word=word, language__name=sourcelang
            ).first()
            trans = '???'
            if word:
                trans = word.synonyms.filter(
                    language__name=targetlang
                ).first()
                if trans:
                    trans = trans.word
            return trans

        context = super().get_context_data(**kwargs)

        sourcelang = kwargs['sourcelang'] or 'ENG'
        targetlang = kwargs['targetlang'] or 'BAR'
        text = kwargs['text'] or ''
        sub = r'\w+'
        translation = re.sub(sub, repl, text)

        context.update({
            'sourcelang': sourcelang,
            'targetlang': targetlang,
            'text': text,
            'translation': translation,
            'languages': Language.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        sourcelang = request.POST.get('sourcelang') or 'BAR'
        targetlang = request.POST.get('targetlang') or 'BAR'
        text = request.POST.get('text', '')

        kwargs = {
            'sourcelang': sourcelang,
            'targetlang': targetlang,
            'text': text,
        }
        # url = reverse_lazy('dictionary:dict_view', kwargs=kwargs)
        # Fixme: reverse doesn't seem to work for some reason
        return HttpResponseRedirect(f'/translate/{sourcelang}/{targetlang}/{text}')
