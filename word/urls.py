

from django.conf.urls import url

from . import views


urlpatterns = [
    # url(r'^$', views.table_view, name='table_view'),
    url(r'^(?P<word_id>[0-9]*)$', views.word_view, name='word_view'),
    url(r'^suggest/?$', views.suggest_view, name='suggest_view'),
]
