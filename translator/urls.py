

from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^((?P<direction>to|from)/(?P<lang>\w{3})/(?P<text>\w+))?$',
        views.TransView.as_view(),
        name='trans_view'
    ),
]
