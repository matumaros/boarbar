

from django.views.generic import DetailView, ListView

from .models import Sentence


class SentenceView(DetailView):
    template_name = 'sentence/display.html'
    http_method_names = ['get']
    model = Sentence

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'translations': self.object.translations.all(),
        })
        return context


class SentenceListView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'sentence/sentence_list.html'

    def get_queryset(self):
        sentences = Sentence.objects.all()
        sentences = sentences.order_by('creation_date')

        return sentences
