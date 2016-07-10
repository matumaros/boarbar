

from django.contrib.auth import authenticate, login as auth, logout as out
from django.shortcuts import render, redirect
from django.views import generic


def home_view(request):
    return render(request, 'share/home.html', {})


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


class DiscussionIndexView(generic.ListView):
    template_name = 'discussion/index.html'


class WordAdd(generic.ListView):
    template_name = 'discussion/wordadd.html'
    context_object_name = 'discussion'

    def get_queryset(self):
        return WordAddition.objects.order_by('-')
