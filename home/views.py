

from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = 'home/home.html'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        print("RRRREQUEST", request)
        print("AAAAARGS", args)
        print("KKKKWARGS", kwargs)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class NewsView(TemplateView):
    template_name = 'home/news.html'
    http_method_names = ['get']


class OgfView(TemplateView):
    template_name = 'home/ogf.html'
    http_method_names = ['get']


class GuestView(TemplateView):
    template_name = 'home/guest.html'
    http_method_names = ['get']


class AboutView(TemplateView):
    template_name = 'home/about.html'
    http_method_names = ['get']


def login(request):
    print("STATUS", status)
    print("REQUEST", request)
    print("POST", request.POST)
    print("GET", request.GET)
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            print("TE AUTENTICO")
        else:
            return redirect(request.POST.get('previous'), {"fail": "fail"})
    else:
        return HttpResponse("hola")
