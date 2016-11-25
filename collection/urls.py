

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CollectionView.as_view(), name='collection_view'),
    url(r'^(?P<pk>[0-9]+)/$', views.ItemView.as_view(), name='item_view'),
    url(
        r'^song/?$',
        views.KindView.as_view(),
        {'kind': 'song'},
        name='song_view'
    ),
    url(
        r'^tongue_twister/?$',
        views.KindView.as_view(),
        {'kind': 'tongue_twister'},
        name='tongue_twister_view'
    ),
    url(
        r'^saying/?$',
        views.KindView.as_view(),
        {'kind': 'saying'},
        name='saying_view'
    ),
    url(
        r'^poem/?$',
        views.KindView.as_view(),
        {'kind': 'poem'},
        name='poem_view'
    ),
]
