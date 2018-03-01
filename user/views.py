import logging

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
from user.notify_user import notify_user
from user.models import UserLanguage, Profile, Language

log = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    http_method_name = ['get']
    model = Profile


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            place = form.cleaned_data.get("place")
            language = form.cleaned_data.get("language")
            print("LANGUAGE ", language.name, type(language.name))
            proficiency = form.cleaned_data.get("proficiency")
            subject = 'Activate Your Servare Account'
            message = render_to_string(
                'user/account_activation_email.html',
                {
                    'user': user,
                    'place': place,
                    'language': language.name,
                    'proficiency': proficiency,
                    'domain': "servare.org",
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode("utf-8"),
                    'token': account_activation_token.make_token(user),
                })
            notify_user(to_email=user.email, message=message, subject=subject)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {'form':form})


def account_activation_sent(request):
    return render(request, 'user/account_activation_sent.html')


def activate(request, uidb64, token, place, language, proficiency):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        user_profile = Profile.objects.create(
            user=user,
            place=place,
            email_confirmed=True,
        )
        language_object = Language.objects.get(name=language)
        user_language = UserLanguage.objects.create(
            user=user_profile,
            language=language_object,
            proficiency=proficiency,
        )

        login(request, user)
        return redirect('/')
    else:
        return render(request, 'user/account_activation_invalid.html')

