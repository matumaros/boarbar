

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.DictIndexView.as_view(), name='index'),
]
