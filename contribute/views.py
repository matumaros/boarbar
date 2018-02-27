

import logging
from django.views.generic import TemplateView

from user.models import Profile, UserLanguage
from word.models import Tag, Word

logger = logging.getLogger(__name__)


class ContribView(TemplateView):
    template_name = 'contribute/main.html'

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
        context["tags"] = Tag.objects.all()
        context["synonyms"] = Word.objects.all()
        return context


def get_highest_language_proficiency(user_languages):
    variants = dict()
    # variants = {
    #             "native": ["es_es"],
    #             "fluent": ["eng_eng", "port_port"],
    #               }

    for user_language in user_languages:
        proficiency = user_language.proficiency
        if proficiency not in variants:
            variants[proficiency] = list()
        default_variant = user_language.language.default_variant
        variants[proficiency].append(default_variant)

    levels = [
        'native',
        'fluent',
        'advanced',
        'intermediate',
        'novice',
        'beginner',
    ]

    for level in levels:
        try:
            default_variant = variants[level][0]
        except (KeyError, IndexError):
            # there is no level in variants or variant[level] is empty
            continue
        return default_variant
