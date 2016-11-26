

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^topics/?$', views.TopicView.as_view(), name='proposal_topic_view'),
    url(r'^proposals/?$', views.ProposalView.as_view(), name='proposals_view'),
    # url(r'^(?P<pk>\d+)$', views.WordView.as_view(), name='word_view'),
]
