

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.WordListView.as_view(), name='word_list_view'),
    url(r'^bare/(?P<pk>\d+)/$', views.BareWordView.as_view(), name='bare_word_view'),
    url(r'^edit/(?P<pk>\d+)/$', views.EditView.as_view(), name='edit_view'),
    url(r'^view/(?P<pk>\d+)$', views.WordView.as_view(), name='word_view'),
    url(r'^suggest/$', views.SuggestView.as_view(), name='suggest_view'),
]
