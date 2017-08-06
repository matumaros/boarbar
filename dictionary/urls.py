

from django.conf.urls import url

from . import views


urlpatterns = [
    # dict without words
    url(
        r'^((?P<sourcelang>\w{3})/(?P<targetlang>\w{3})/(?P<word>.*))?$',
        views.DictView.as_view(),
        name='dict_view'
    ),
    # dict with origin language, target language and word
    # url(
    #     r'^(?P<sourcelang>[A-Z]{3})/(?P<word>.*)$',
    #     views.DictAfterSearchView.as_view(),
    #     name='dict_view_after_search'
    # ),
]
