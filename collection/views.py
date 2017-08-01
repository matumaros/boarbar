

from django.views.generic import TemplateView, ListView, DetailView

from .models import Collection


class CollectionView(DetailView):
    template_name = 'collection/detail.html'
    http_method_names = ['get']
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'collection': self.object,
        })
        return context

class CollectionListView(TemplateView):
    template_name = 'collection/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        collections = Collection.objects.all()

        context.update({
            'collections': collections,
        })
        return context
