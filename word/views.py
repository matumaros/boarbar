from django.views.generic import DetailView

from .models import BavarianWord


class IndexView(DetailView):
    template_name = 'word/main.html'
    http_methods_name = ['get']
    model = BavarianWord
