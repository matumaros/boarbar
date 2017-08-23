

from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test

from . import views


urlpatterns = [
    url(r'^$', views.WordListView.as_view(), name='word_list_view'),
    url(r'^bare/(?P<pk>\d+)/$', views.BareWordView.as_view(), name='bare_word_view'),
    url(r'^edit/(?P<pk>\d+)/$',
        user_passes_test(
            lambda u: u.is_authenticated and u.profile.reputation >= 100,
            login_url=''
        )(
            views.EditView.as_view()
        ),
        name='edit_view'),
    url(r'^view/(?P<pk>\d+)$', views.WordView.as_view(), name='word_view'),
    url(r'^suggest/$', views.SuggestView.as_view(), name='suggest_view'),
]
