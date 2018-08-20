

from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import render
from .models import Collection


class CollectionView(DetailView):
    template_name = 'collection/detail.html'
    http_method_names = ['get']
    model = Collection

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'collection': self.object,
            'text': self.object.processed_text(
                '<a class={type} onclick="show_word_detail({id})">{word}</a>'
            )
        })
        return context

class CollectionListView(TemplateView):
    template_name = 'collection/main.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(kwargs)
        collection_types = Collection.objects.all().distinct("type")

        context.update({
            'collection_types': collection_types,
        })
        return context

def collection_view(request, collection_type):
    collections = Collection.objects.filter(type=collection_type)
    print(collections)
    context = {"collections": collections}
    collection_types = Collection.objects.all().distinct("type")
    context["collection_types"] = collection_types
    return render(request, "collection/main.html", context)
