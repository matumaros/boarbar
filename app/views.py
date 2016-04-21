

from django.shortcuts import render
from django.views import generic


def home_view(request):
    return render(request, 'app/home.html', {})


class DiscussionIndexView(generic.ListView):
    template_name = 'discussion/index.html'


class WordAdd(generic.ListView):
    template_name = 'discussion/wordadd.html'
    context_object_name = 'discussion'

    def get_queryset(self):
        return WordAddition.objects.order_by('-')
