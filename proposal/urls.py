

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^topics/?$', views.TopicView.as_view(), name='proposal_topic_view'),
    url(r'^proposals/?$', views.ProposalView.as_view(), name='proposals_view'),
    url(
        r'^topic/(?P<pk>\d+)$',
        views.TopicDetailView.as_view(),
        name='proposal_topic_detail_view',
    ),
    url(
        r'^proposal/(?P<pk>\d+)$',
        views.ProposalDetailView.as_view(),
        name='proposal_detail_view',
    ),
]
