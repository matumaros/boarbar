from django.conf.urls import url

from . import views


app_name = "contribute"

urlpatterns = [
    url(
        r'^$',
        views.ContribView.as_view(),
        name='contrib_view'
    ),
    # dict with origin language, target language and word
    # url(
    #     r'^(?P<sourcelang>[A-Z]{3})/(?P<word>.*)$',
    #     views.DictAfterSearchView.as_view(),
    #     name='dict_view_after_search'
    # ),
]
