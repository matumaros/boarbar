
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from user.tokens import account_activation_token
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
            user = form.save()
            user.is_active = False
            user.save()

            subject = 'Activate Your Servare Account'
            message = render_to_string(
                'user/account_activation_email.html',
                context={
                    'user': user,
                    'domain': "servare.org",
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message, from_email="malaria@manolo.rocks")

            language = form.cleaned_data.get("language")
            place = form.cleaned_data.get("place")
            proficiency = form.cleaned_data.get("proficiency")
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            django_user = authenticate(username=username, password=raw_password)
            print(django_user, username, raw_password, "$$$$$$$$$")
            user_profile = Profile.objects.create(
                user=django_user,
                place=place,
            )
            user_language = UserLanguage.objects.create(
                user=user_profile,
                language=language,
                proficiency=proficiency,
            )
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {'form':form})


def activate(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        user_profile = Profile.objects.get(user=user)
        user_profile.email_confirmed = True
        user_profile.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user/account_activation_invalid.html')

