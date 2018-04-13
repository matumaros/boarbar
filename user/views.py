import logging

from django.http import HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from user.tokens import account_activation_token
from user.forms import SignUpForm
from user.notify_user import notify_user
from user.models import UserLanguage, Profile
from language.models import Language

log = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    http_method_name = ['get']
    model = Profile

    def get(self, request, *args, **kwargs):
        profile_id = int(kwargs["pk"])
        if request.user.profile.id != profile_id:
            return HttpResponseNotFound("You cannot view other user's profile")

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data.get("description")
            place = form.cleaned_data.get("place")
            language = form.cleaned_data.get("language")
            proficiency = form.cleaned_data.get("proficiency")

            user = form.save(commit=False)
            if User.objects.filter(email=user.email).exists():
                return HttpResponseBadRequest("Somebody has already registered with this email")
            elif User.objects.filter(username=user.username).exists():
                return HttpResponseBadRequest("Somebody has already used this username")

            user.is_active = False
            user.save()

            profile = Profile(
                user=user,
                description=description,
                place=place,
            )
            profile.save()

            user_language = UserLanguage(
                user=profile,
                language=Language.objects.get(name=language),
                proficiency=proficiency,
            )
            user_language.save()

            subject = 'Activate Your Servare Account'
            message = render_to_string(
                'user/account_activation_email.html',
                {
                    'user': user,
                    'domain': request.META['HTTP_HOST'],
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


def activate(request, uidb64, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)
        return redirect('/')
    else:
        return render(request, 'user/account_activation_invalid.html')

