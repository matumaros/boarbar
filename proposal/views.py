

from django.views.generic import ListView, DetailView

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


class TopicDetailView(DetailView):
    template_name = 'proposal/topic_detail.html'
    http_method_names = ['get']
    model = ProposalTopic

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'proposals': self.object.proposals.all(),
        })
        return context


class ProposalDetailView(DetailView):
    template_name = 'proposal/proposal_detail.html'
    http_method_names = ['get']
    model = Proposal
