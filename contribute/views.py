import json
from django.views.generic import TemplateView
from django.http import HttpResponse

from user.models import Profile, UserLanguage
from word.models import Tag, Word, WordVersion, Description


class ContribView(TemplateView):
    template_name = 'contribute/main.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        try:
            user_profile = Profile.objects.get(user=request.user)
        except TypeError:
            user_profile = None

        if user_profile:
            user_language = UserLanguage.objects.get(user=user_profile)
            if user_language.is_moderator:
                user_moderator = True
            else:
                user_moderator = False
            context["user_moderator"] = user_moderator
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["synonyms"] = Word.objects.all()
        context["version"] = WordVersion.objects.all()
        return context
