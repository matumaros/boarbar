

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home_view'),
    url(r'^news/?$', views.NewsView.as_view(), name='news_view'),
    url(r'^ogf/?$', views.OgfView.as_view(), name='ogf_view'),
    url(r'^guest/?$', views.GuestView.as_view(), name='guest_view'),
    url(r'^about/?$', views.AboutView.as_view(), name='about_view'),
]
