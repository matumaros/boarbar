from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login as auth, logout as out
from django.shortcuts import render, redirect
from django.http import HttpResponse


def login(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth(request, user)
                    return redirect(request.POST['previous'])
                else:
                    return HttpResponse('Your account is disabled.')
            else:
                return HttpResponse('Invalid login details supplied.')
    return redirect('/admin/')


def logout(request):
    out(request)
    return redirect(request.POST['previous'])

class NotExistingView(TemplateView):
    template_name = 'share/not_existing.html'
    http_methods_name = ['get']
