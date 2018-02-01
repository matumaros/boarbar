from django.views.generic import TemplateView


class ContribView(TemplateView):
    template_name = 'contribute/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context