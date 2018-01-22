

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'
    http_method_names = ['get']


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

