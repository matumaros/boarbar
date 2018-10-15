import operator
from functools import reduce

from django.db import IntegrityError
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Collection, CollectionType
from user.models import Profile
from .forms import CollectionForm


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
            ),
            'col_type': self.object.type
        })
        return context


def keyword_filtered(request):
    collection_words = []
    keywords = ""
    if request.GET:
        keywords = request.GET.get("keywords", '')
        if keywords:
            keywords = keywords.split()
            collection_words = Collection.objects.filter(
                Q(reduce(operator.or_, (Q(title__contains=x) for x in keywords))) |
                Q(reduce(operator.or_, (Q(text__contains=x) for x in keywords)))
            )
    context = dict()
    context["collection_types"] = get_collection_types()
    context["collection_words"] = collection_words

    first_collection_obj = Collection.objects.all().first()
    if first_collection_obj and keywords == "":
        # eg. poem
        collection_type = first_collection_obj.type
        # eg. all poems
        collections = Collection.objects.filter(type=collection_type)
        context["collections"] = collections
        context["active_collection"] = collection_type
        print("context", context)
    else:
        context["collections"] = []
        context["active_collection"] = None
    return render(request, "collection/main.html", context)


def type_filtered(request, collection_type):
    collection_type = collection_type.replace("_", " ")
    collections = Collection.objects.filter(type__name=collection_type)
    context = {"collections": collections}
    context["collection_types"] = get_collection_types()
    context["active_collection"] = collection_type
    return render(request, "collection/main.html", context)


def get_collection_types():
    collection_types = Collection.objects.all().distinct(
        "type").values_list("type__name", flat=True)
    collection_types = [
        {
            "path": collection_type.replace(" ", "_"),
            "name": collection_type,
        }
        for collection_type in collection_types
    ]
    return collection_types


def new_collection(request):
    if request.POST:
        form = CollectionForm(request.POST)
        if form.is_valid():
            print("####POST", request.POST)
            title = request.POST.get("title").lower()
            print(title)
            author = request.POST.get("author")
            text = request.POST.get("text").lower()
            type = request.POST.get("type")

            type = CollectionType.objects.get(name=type)
            reporter = Profile.objects.get(user=request.user)

            try:
                Collection.objects.create(
                    title=title,
                    author=author,
                    text=text,
                    type=type,
                    reporter=reporter
                )
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "A collection \
                with the same title, text and type already exist")
                return redirect('/collection/new_collection/')

            return redirect('/collection/')

    form = CollectionForm(request.POST or None)

    context = {
        'form': form,
        'collection_types': get_collection_types(),
    }
    return render(request, "collection/collection_form.html", context)

