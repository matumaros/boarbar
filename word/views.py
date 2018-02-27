

import re

from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Word, Description, WordVersion, WordLocation, Tag
from .forms import WordForm
from language.models import Language


class WordView(DetailView):
    template_name = 'word/display.html'
    http_method_names = ['get']
    model = Word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'descriptions': self.object.desc.all(),
            'synonyms': self.object.synonyms.all(),
            'locations': self.object.locations.all(),
        })
        return context


@method_decorator(login_required, name='dispatch')
class SuggestView(TemplateView):
    """
    User story:
      Word: Kusko
      WordVersion: Quechua Ayacuchano where the word they use is Kusko
      Language: Quechua
    """
    template_name = 'word/suggest.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'versions': WordVersion.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        word_obj = None
        if request.method == "POST" and "file" in request.FILES:
            form = WordForm(request.POST, request.FILES)
            if form.is_valid():
                print("$"*10, "form is valid")
                # myfile = request.FILES["myfile"]
                word_obj = form.save(commit=False)
                word_obj.submitter = request.user.profile
                word_obj.audio = request.FILES["file"]
                word_obj.save()
            else:
                print("$" * 10, form.errors)

        word = request.POST.get('word')
        tags = request.POST.getlist('tags')
        ipa = request.POST.get('ipa')
        default_variant_str = request.POST.get('language')
        location = request.POST.get('location')
        synonyms = request.POST.getlist('synonyms')
        #wiktionary_link = request.POST.get('wiktionary_link')

        desc_list = self.create_descriptions(request)

        language_object = Language.objects.get(default_variant=default_variant_str)

        # TODO: so far all word versions of a language can be associated with
        # TODO: only one variant (the language's own default variant)
        word_version = WordVersion.objects.filter(language=language_object)[0]

        if word_obj:
            word_obj.word=word
            word_obj.ipa=ipa
            word_obj.status='SUG'
            word_obj.version=word_version
            word_obj.save()
                #wiktionary_link = wiktionary_link
        else:
            word_obj = Word.objects.create(
                word=word,
                ipa=ipa,
                status='SUG',
                version=word_version,
                submitter=request.user.profile,
                #wiktionary_link = wiktionary_link,
            )

        for desc in desc_list:
            word_obj.desc.add(desc)

        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(name=tag.lower())
            word_obj.tags.add(tag_object)

        for syn in synonyms:
            syn_object, _ = Word.objects.get_or_create(
                submitter=request.user.profile,
                word=syn.lower(),
            )
            word_obj.synonyms.add(syn_object)
        if location:
            location = WordLocation.objects.create(
                word=word_obj,
                place=location,
                submitter=request.user.profile,
            )

        url = reverse_lazy('word:word_view', kwargs={'pk': word_obj.id})
        return HttpResponseRedirect(url)

    def create_descriptions(self, request):
        """Function to generate list of description objects for one word,
        each description object is in a different language and contains both
        short and long description strings

        {
            'english': {'desc_short': 'short mouse', 'desc_long': 'long mouse'},
            'spanish': {'desc_short': 'raton corto', 'desc_long': 'raton largo'}
        }
        :param request: original django request
        :return: list of Description objects
        """
        descriptions = dict()
        for key in request.POST.keys():
            if "desc_long" in key:
                desc_long_string = request.POST.get(key)
                language = key.split("_")[-1]
                if language not in descriptions:
                    descriptions[language] = dict()
                descriptions[language]["desc_long"] = desc_long_string

            if "desc_short_" in key:
                # desc_short_spanish
                desc_short_string = request.POST.get(key)
                language = key.split("_")[-1]
                if language not in descriptions:
                    descriptions[language] = dict()
                descriptions[language]["desc_short"] = desc_short_string
        desc_list = []
        for language, language_desc in descriptions.items():
            language_obj = Language.objects.get(name=language)
            desc, _ = Description.objects.get_or_create(
                language=language_obj,
                short=language_desc["desc_short"],
                extended=language_desc["desc_long"],
            )
            desc_list.append(desc)
        return desc_list


class EditView(UpdateView):
    model = Word
    fields = [
        'word', 'ipa', 'desc', 'tags', 'audio', 'wiktionary_link', 'synonyms'
    ]
    template_name_suffix = '_update_form'

    # template_name = 'word/edit.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     pk = kwargs.get('pk')
    #     word = Word.objects.get(pk=pk)

    #     context.update({
    #         'word': word,
    #         'versions': WordVersion.objects.all(),
    #     })
    #     return context

    # def post(self, request, *args, **kwargs):
    #     word = request.POST.get('word')
    #     ipa = request.POST.get('ipa')
    #     version = request.POST.get('version')
    #     location = request.POST.get('location')
    #     description_short = request.POST.get('desc_short')
    #     description_long = request.POST.get('desc_long')

    #     version = WordVersion.objects.get(pk=version)

    #     desc = Description.objects.create(
    #         short=description_short,
    #         extended=description_long,
    #         language=version.language,
    #     )
    #     word = Word.objects.create(
    #         word=word,
    #         ipa=ipa,
    #         status='SUG',
    #         version=version,
    #         submitter=request.user.profile,
    #     )
    #     word.desc.add(desc)
    #     if location:
    #         location = WordLocation.objects.create(
    #             word=word,
    #             place=location,
    #             submitter=request.user.profile,
    #         )

    #     url = reverse_lazy('word:word_view', kwargs={'pk': word.id})
    #     return HttpResponseRedirect(url)


class WordListView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'word/word_list.html'

    def get_queryset(self):
        words = Word.objects.all()
        words = words.order_by('creation_date')

        return words


class BareWordView(DetailView):
    template_name = 'word/word_detail.html'
    http_method_names = ['get']
    model = Word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'descriptions': self.object.desc.all(),
            'translations': self.object.translations.all(),
        })
        return context
