

from django.contrib.auth import logout as out
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View


class Logout(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        out(request)

        previous = request.POST.get('previous', reverse('home:home_view'))
        return HttpResponseRedirect(previous)


class NotExisting(TemplateView):
    http_method_names = ['get']
    template_name = 'share/not_existing.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["request_url"] = request.path
        return self.render_to_response(context)