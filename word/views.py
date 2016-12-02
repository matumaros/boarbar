

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, ListView

from .models import Word, Description
from language.models import Language


class WordView(DetailView):
    template_name = 'word/display.html'
    http_method_names = ['get']
    model = Word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'descriptions': self.object.desc.all(),
            'translations': self.object.translations.all(),
        })
        return context


class SuggestView(TemplateView):
    template_name = 'word/suggest.html'
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        word = request.POST.get('word')
        description_short = request.POST.get('desc_short')
        description_long = request.POST.get('desc_long')

        language = Language.objects.get(name='BAR')
        desc = Description.objects.create(
            short=description_short,
            extended=description_long,
            language=language,
        )
        word = Word.objects.create(
            word=word,
            status='SUG',
            version='boarV1',
        )
        word.desc.add(desc)

        url = reverse_lazy('word:word_view', kwargs={'pk': word.id})
        return HttpResponseRedirect(url)


class WordListView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'word/word_list.html'

    def get_queryset(self):
        words = Word.objects.all()
        words = words.order_by('creation_date')

        return words
