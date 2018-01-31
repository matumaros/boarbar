from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView


class ContribView(TemplateView):
    template_name = 'contribute/main.html'
    http_method_names = ['get', 'post']

    def post(self, request, *args, **kwargs):
        word = request.POST.get('word', '')

        kwargs = {
            'word': word,
        }
        # url = reverse_lazy('dictionary:dict_view', kwargs=kwargs)
        # Fixme: reverse doesn't seem to work for some reason
        return HttpResponseRedirect(f'/dict/{sourcelang}/{targetlang}/{word}')
