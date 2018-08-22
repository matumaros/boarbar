import operator
from functools import reduce

from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
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


def keyword_filtered(request):
    collection_words = []
    if request.GET:
        keywords = request.GET.get("keywords", '')
        if keywords:
            keywords = keywords.split()
            collection_words = Collection.objects.filter(
                Q(reduce(operator.or_, (Q(title__contains=x) for x in keywords))) |
                Q(reduce(operator.or_, (Q(text__contains=x) for x in keywords)))
            )
    context = dict()
    context["collection_types"] = {i.type: i.type.replace("_", " ") for i in Collection.objects.all().distinct("type")}
    context["collection_words"] = collection_words
    return render(request, "collection/main.html", context)


def type_filtered(request, collection_type):
    collections = Collection.objects.filter(type=collection_type)
    context = {"collections": collections}
    collection_types = {i.type: i.type.replace("_", " ") for i in Collection.objects.all().distinct("type")}
    context["collection_types"] = collection_types

    return render(request, "collection/main.html", context)
