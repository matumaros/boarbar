

from django.conf.urls import url

from . import views


app_name = "collection"

urlpatterns = [
    url(r'^$', views.CollectionListView.as_view(), name='collection_list_view'),
    url(r'^(?P<collection_type>\w+)$', views.collection_view, name='collection_list_view'),
    url(r'^(?P<pk>[0-9]+)/$', views.CollectionView.as_view(), name='collection_view'),

]
