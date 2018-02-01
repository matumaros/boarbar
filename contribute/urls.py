from django.conf.urls import url

from . import views


app_name = "contribute"

urlpatterns = [
    url(
        r'^$',
        views.ContribView.as_view(),
        name='contrib_view'
    ),
]
