

from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Word, Description, WordVersion, WordLocation, Tag
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
    template_name = 'word/suggest.html'
    http_method_names = ['get', 'post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'versions': WordVersion.objects.all(),
        })
        return context

    def post(self, request, *args, **kwargs):
        uploaded_file_url = None
        if request.method == "POST" and "myfile" in request.FILES:
            myfile = request.FILES["myfile"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            if filename.endswith(".mp3") or filename.endswith(".wma") or\
                filename.endswith(".wav") or filename.endswith(".m4a"):
                    uploaded_file_url = fs.url(filename)
            else:
                filename = None
                uploaded_file_url = fs.url(filename)

        word = request.POST.get('word')
        tags = request.POST.getlist('tags')
        ipa = request.POST.get('ipa')
        version_id = request.POST.get('version')
        location = request.POST.get('location')
        description_long = request.POST.getlist('desc_long')
        synonyms = request.POST.getlist('synonyms')
        wiktionary_link = request.POST.get('wiktionary_link')

        print("====================desc short")
        descriptions_list = []
        for key in request.POST.keys():
            if "desc_short_" in key:
                # desc_short_spanish
                desc_short_string = request.POST.get(key)
                language_string = key.split("_")[-1]
                language_obj = Language.objects.get(name=language_string)
                desc, _ = Description.objects.get_or_create(
                    short=desc_short_string.strip(),
                    #extended=potooo
                    language=language_obj
                )
                descriptions_list.append(desc)

        version_object = WordVersion.objects.get(pk=version_id)

        word = Word.objects.create(
            word=word,
            ipa=ipa,
            status='SUG',
            version=version_object,
            audio=uploaded_file_url,
            submitter=request.user.profile,
            wiktionary_link = wiktionary_link,
        )
        for desc in descriptions_list:
            word.desc.add(desc)

        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(name=tag.lower())
            word.tags.add(tag_object)

        for syn in synonyms:
            syn_object, _ = Word.objects.get_or_create(
                submitter=request.user.profile,
                word=syn.lower(),
            )
            word.synonyms.add(syn_object)
        if location:
            location = WordLocation.objects.create(
                word=word,
                place=location,
                submitter=request.user.profile,
            )

        url = reverse_lazy('word:word_view', kwargs={'pk': word.id})
        return HttpResponseRedirect(url)


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
