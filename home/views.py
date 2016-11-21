from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'home/home.html'
    http_methods_name = ['get']


class NewsView(TemplateView):
    template_name = 'home/news.html'
    http_methods_name = ['get']


class OgfView(TemplateView):
    template_name = 'home/ogf.html'
    http_methods_name = ['get']


class GuestView(TemplateView):
    template_name = 'home/guest.html'
    http_methods_name = ['get']


class AboutView(TemplateView):
    template_name = 'home/about.html'
    http_methods_name = ['get']
