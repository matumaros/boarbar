

from django.views import generic

from .models import Word


class DictIndexView(generic.ListView):
    template_name = 'dictionary/index.html'

    def get_queryset(self):
        return Word.objects
