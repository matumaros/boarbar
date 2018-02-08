from django.views.generic import TemplateView

from word.models import Tag, WordVersion

class ContribView(TemplateView):
    template_name = 'contribute/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context["versions"] = WordVersion.objects.all()
        return context