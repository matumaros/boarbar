

from django.conf.urls import url

from . import views


app_name = "proposal"

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
    url(
        r'^proposal/new/$',
        views.ProposalAddView.as_view(),
        name='proposal_add_view',
    ),
    url(
        r'^proposal/edit/(?P<pk>\d+)$',
        views.ProposalEditView.as_view(),
        name='proposal_edit_view',
    ),
]
