
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from user.forms import SignUpForm

from user.models import UserLanguage, Profile


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    http_method_name = ['get']
    model = Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            language = form.cleaned_data.get("language")
            place = form.cleaned_data.get("place")
            proficiency = form.cleaned_data.get("proficiency")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            django_user = authenticate(username=username, password=raw_password)
            login(request, django_user)
            user_profile = Profile.objects.create(
                user=django_user,
                place=place,
            )
            user_language = UserLanguage.objects.create(
                user=user_profile,
                language=language,
                proficiency=proficiency,
            )
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {'form':form})


