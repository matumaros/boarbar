

from django.shortcuts import render

from .models import CollectionItem


def collection_view(request):
    songs = CollectionItem.objects.filter(kind='song')
    tongue_twisters = CollectionItem.objects.filter(kind='tongue_twister')
    sayings = CollectionItem.objects.filter(kind='saying')
    poems = CollectionItem.objects.filter(kind='poem')
    kwargs = {
        'songs': songs,
        'tongue_twisters': tongue_twisters,
        'sayings': sayings,
        'poems': poems,
    }
    return render(request, 'collection/main.html', kwargs)


def kind_view(request, kind):
    items = CollectionItem.objects.filter(kind=kind).order_by('creation_date')
    kwargs = {
        'items': items,
    }
    return render(request, 'collection/{}s.html'.format(kind), kwargs)


def item_view(request, item_id):
    item = CollectionItem.objects.get(pk=item_id)
    kwargs = {
        'item': item,
    }
    return render(request, 'collection/item.html', kwargs)
