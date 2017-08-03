

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.WordListView.as_view(), name='word_list_view'),
    url(r'^(?P<pk>\d+)$', views.WordView.as_view(), name='word_view'),
    url(r'^suggest/$', views.SuggestView.as_view(), name='suggest_view'),
]
