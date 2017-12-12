

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CollectionListView.as_view(), name='collection_list_view'),
    url(r'^(?P<pk>[0-9]+)/$', views.CollectionView.as_view(), name='collection_view'),
]
