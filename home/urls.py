

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home_view, name='home_view'),
    url(r'^news/?$', views.news_view, name='news_view'),
    url(r'^ogf/?$', views.ogf_view, name='ogf_view'),
    url(r'^guest/?$', views.guest_view, name='guest_view'),
    url(r'^about/?$', views.about_view, name='about_view'),
]
