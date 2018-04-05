

import logging

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from language.models import Language
from user.models import Profile, UserLanguage
from word.models import Word, Tag
from contribute.views import get_highest_language_proficiency

logger = logging.getLogger(__name__)


class DictView(TemplateView):
    template_name = 'dictionary/main.html'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            user_profile = Profile.objects.get(user=request.user)
        except TypeError:
            logger.info("user does not have profile")

        else:
            user_languages = UserLanguage.objects.filter(user=user_profile)
            user_moderator = False

            for user_language in user_languages:
                if user_language.is_moderator:
                    user_moderator = True
                    break
            context["user_moderator"] = user_moderator
            context["user_languages"] = user_languages

            default_variant = get_highest_language_proficiency(user_languages)
            context["default_variant"] = default_variant

        return self.render_to_response(context)


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
