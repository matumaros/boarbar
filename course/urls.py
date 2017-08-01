

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.CourseListView.as_view(), name='course_list_view'),
    # url(r'^(?P<pk>[0-9]+)/$', views.CourseView.as_view(), name='course_view'),
]
