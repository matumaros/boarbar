from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', views.IndexView.as_view(), name='word_view'),
]
