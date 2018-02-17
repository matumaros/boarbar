

import logging
from django.views.generic import TemplateView

from user.models import Profile, UserLanguage
from word.models import Tag, Word, WordVersion

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
            context["language"] = user_languages
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["synonyms"] = Word.objects.all()
        context["version"] = WordVersion.objects.all()
        return context
