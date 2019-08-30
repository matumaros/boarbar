import logging
import operator
from functools import reduce
import re

from django.db import IntegrityError
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect

from word.views import add_default_variant
from word.models import Tag, Word
from .models import Collection, CollectionType
from user.models import Profile
from .forms import CollectionForm


logger = logging.getLogger(__name__)


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
    #to delete <br> from html text
    for col in collection_words:
        col.text = re.sub('<br class="left">', " ", col.text)

    first_collection_obj = Collection.objects.all().first()
    if first_collection_obj and keywords == "":
        # eg. poem
        collection_type = first_collection_obj.type
        # eg. all poems
        collections = []
        for collection_type in Collection.objects.all().distinct("type"):
            collection_sample = Collection.objects.filter(type=collection_type.type).order_by("-id")[0:3]
            collections.extend(list(collection_sample))
        context["collections"] = collections
        context["active_collection"] = collection_type
        # to delete <br> from html text
        for col in collections:
            col.text = re.sub('<br class="left">', " ", col.text)

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
    #to delete <br> from html text
    for col in collections:
        col.text = re.sub('<br class="left">', " ", col.text)
    return render(request, "collection/main.html", context)


def get_collection_types():
    collection_types = CollectionType.objects.all().values_list("name", flat=True)
    collection_types = [
        {
            "path": collection_type.replace(" ", "_"),
            "name": collection_type,
        }

        for collection_type in collection_types
            if collection_type
    ]
    return collection_types


def new_collection(request):
    if not request.user.is_authenticated:
        return render(request, 'share/need_login.html')

    if request.POST:
        form = CollectionForm(request.POST)
        if form.is_valid():
            title = request.POST.get("title").lower()
            author = request.POST.get("author").lower() or ""
            text = request.POST.get("text").lower()
            type = request.POST.get("type")

            type = CollectionType.objects.get(name=type)
            reporter = Profile.objects.get(user=request.user)
            if title.strip() == "" or text == "":
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You need to enter a title and text for the collection")
                return redirect('/collection/new_collection/')

            try:
                Collection.objects.create(
                    title=title,
                    author=author,
                    text=text,
                    type=type,
                    reporter=reporter
                )

            except IntegrityError:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "A collection with the same title, text and type already exist")
                return redirect('/collection/new_collection/')

            return redirect('/collection/')

    try:
        user_profile = Profile.objects.get(user=request.user)
    except TypeError:
        logger.info("user does not have profile")

    form = CollectionForm(request.POST or None)

    context = {
        'form': form,
        'collection_types': get_collection_types(),
    }
    context = add_default_variant(context, user_profile)
    context["tags"] = Tag.objects.all()
    context["synonyms"] = Word.objects.all()
    return render(request, "collection/collection_form.html", context)


def edit_collection(request, pk):
    collection = Collection.objects.get(id=pk)

    try:
        user_profile = Profile.objects.get(user=request.user)
    except TypeError:
        logger.info("user does not have profile")

    form = CollectionForm(request.POST or None)
    if form.is_valid():
        collection.title = request.POST.get("title").lower()
        collection.author = request.POST.get("author").lower() or ""
        collection.text = request.POST.get("text").lower()
        type = request.POST.get("type")
        collection.type = CollectionType.objects.get(name=type)
        collection.reporter = Profile.objects.get(user=request.user)
        collection.save()

        return redirect("/collection/")

    context = {
        'edit':True,
        'collection': collection,
        'form': form,
        'collection_types': get_collection_types(),
    }
    context = add_default_variant(context, user_profile)
    context["tags"] = Tag.objects.all()
    context["synonyms"] = Word.objects.all()
    return render(request, "collection/collection_form.html", context)


