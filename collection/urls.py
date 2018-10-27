

from django.conf.urls import url

from . import views


app_name = "collection"

urlpatterns = [
    url(r'^$', views.keyword_filtered, name='keyword_filtered'),
    url(r'^(?P<collection_type>\w+)$', views.type_filtered, name='type_filtered'),
    url(r'^(?P<pk>[0-9]+)/$', views.CollectionView.as_view(), name='collection_view'),
    url(r'^new_collection/$', views.new_collection, name='new_collection'),

]
