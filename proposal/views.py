

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, TemplateView

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


class ProposalAddView(CreateView):
    template_name = 'proposal/proposal_add.html'
    http_method_names = ['get', 'post']
    fields = ['title', 'description', 'topic']
    success_url = '/proposal/proposals/'
    model = Proposal

    def form_valid(self, form):
        form.instance.created_by = self.request.user.profile
        return super().form_valid(form)


class ProposalEditView(DetailView):
    template_name = 'proposal/proposal_edit.html'
    http_method_names = ['get', 'post']
    model = Proposal

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.title = request.POST.get('title', '')
        obj.description = request.POST.get('description', '')
        obj.save()

        kwargs = {'pk': obj.id}
        url = reverse_lazy('proposal:proposal_detail_view', kwargs=kwargs)
        return HttpResponseRedirect(url)
