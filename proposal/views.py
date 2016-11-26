

from django.views.generic import ListView

from .models import ProposalTopic, Proposal


class TopicView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'proposal/topic_list.html'

    def get_queryset(self):
        topics = ProposalTopic.objects.all()
        topics = topics.order_by('creation_date')

        return topics


class ProposalView(ListView):
    http_method_names = ['get']
    paginate_by = 10
    template_name = 'proposal/proposal_list.html'

    def get_queryset(self):
        topics = Proposal.objects.all()
        topics = topics.order_by('creation_date')

        return topics
