

from django.conf.urls import url

from .. import views

urlpatterns = [
    url(r'^$', views.DiscussionIndexView.as_view(), name='index'),
    url(r'wordadd/?$', views.WordAdd.as_view(), name='wordadd')
]
