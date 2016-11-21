

from django.conf.urls import url

from . import views


urlpatterns = [
    # dict without words
    url(r'^$', views.DictView.as_view(), name='dict_view'),
    # dict with origin language, target language and word
    url(
        r'^(?P<sourcelang>[A-Z]{3})/(?P<word>.+)$',
        views.DictSearhView.as_view(),
        name='dict_search_view'
    ),
]
