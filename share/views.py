

from django.contrib.auth import logout as out
from django.shortcuts import render, redirect


def logout(request):
    out(request)
    return redirect(request.POST['previous'])


def not_existing(request):
    return render(request, 'share/not_existing.html', {})
