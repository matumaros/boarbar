

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.SentenceListView.as_view(), name='sentence_list_view'),
    url(r'^(?P<pk>\d+)$', views.SentenceView.as_view(), name='sentence_view'),
]
