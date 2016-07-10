

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.collection_view, name='collection_view'),
    url(r'^(?P<item_id>[0-9])$', views.item_view, name='item_view'),
    url(
        r'^song/?$',
        views.kind_view,
        {'kind': 'song'},
        name='song_view'
    ),
    url(
        r'^tongue_twister/?$',
        views.kind_view,
        {'kind': 'tongue_twister'},
        name='tongue_twister_view'
    ),
    url(
        r'^saying/?$',
        views.kind_view,
        {'kind': 'saying'},
        name='saying_view'
    ),
    url(
        r'^poem/?$',
        views.kind_view,
        {'kind': 'poem'},
        name='poem_view'
    ),
]
