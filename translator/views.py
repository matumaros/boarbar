

import re

from django.views.generic import TemplateView

from word.models import Word
from language.models import Language


class TransView(TemplateView):
    template_name = 'translator/display.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        def repl(match):
            word = match.group()
            if direction == 'to':
                word = Word.objects.filter(word=word).first()
                if word:
                    trans = word.translations.filter(
                        language__name=lang).first()
                    if trans:
                        trans = trans.word
                    else:
                        trans = '???'
                else:
                    trans = '???'
            elif direction == 'from':
                word = Translation.objects.filter(
                    word=word, language__name=lang).first()
                if word:
                    trans = word.translation.word
                else:
                    trans = '???'

            return trans

        direction = kwargs['direction'] or 'to'
        lang = kwargs['lang'] or 'ENG'
        context = super().get_context_data(**kwargs)
        text = kwargs['text'] or ''
        sub = r'\w+'
        translation = re.sub(sub, repl, text)

        context.update({
            'direction': direction,
            'lang': lang,
            'text': text,
            'translation': translation,
        })
        return context
