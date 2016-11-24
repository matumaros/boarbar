

from django.views.generic import TemplateView, ListView, DetailView

from .models import CollectionItem


class CollectionView(TemplateView):
    template_name = 'collection/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        songs = CollectionItem.objects.filter(kind='song')
        tongue_twisters = CollectionItem.objects.filter(kind='tongue_twister')
        sayings = CollectionItem.objects.filter(kind='saying')
        poems = CollectionItem.objects.filter(kind='poem')

        context.update({
            'songs': songs,
            'tongue_twisters': tongue_twisters,
            'sayings': sayings,
            'poems': poems,
        })
        return context


class KindView(ListView):
    http_method_names = ['get']
    paginate_by = 10

    def _get_kind(self):
        return self.kwargs.get('kind')

    def get_template_names(self):
        kind = self._get_kind()
        template_name = 'collection/{}s.html'.format(kind)

        return [template_name]

    def get_queryset(self):
        kind = self._get_kind()
        collection_items = CollectionItem.objects.filter(kind=kind)
        collection_items = collection_items.order_by('creation_date')

        return collection_items


class ItemView(DetailView):
    template_name = 'collection/item.html'
    http_method_names = ['get']
    model = CollectionItem
