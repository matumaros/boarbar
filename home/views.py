

from django.shortcuts import render


def home_view(request):
    return render(request, 'home/home.html', {})

def news_view(request):
    return render(request, 'home/news.html', {})

def ogf_view(request):
    return render(request, 'home/ogf.html', {})

def guest_view(request):
    return render(request, 'home/guest.html', {})
    
def about_view(request):
    return render(request, 'home/about.html', {})
