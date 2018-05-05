import logging

from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, UpdateView, View
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from user.tokens import account_activation_token
from user.forms import SignUpForm, UpdateProfileForm
from user.notify_user import notify_user
from user.models import UserLanguage, Profile
from language.models import Language

log = logging.getLogger(__name__)


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    http_method_name = ['get']
    model = Profile


class EditUserProfileView(View):
    model = Profile, UserLanguage
    form_class = UpdateProfileForm
    template_name = "user/profile_edit.html"
    id = None

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=user)
        user_language = UserLanguage.objects.filter(user=profile)
        initial = {"description": profile.description, "place":profile.place,
                   "language": list(user_language.values_list("language", flat=True))}
        print("#######profile", user_language.values_list("proficiency"))

        form = self.form_class(initial=initial)
        return render(
            request,
            self.template_name,
            {'form': form, 'pk': kwargs["pk"], "proficiency": user_language.values("proficiency")})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=self.kwargs['pk'])
            profile = Profile.objects.get(user=user)
            profile.description = form.cleaned_data["description"]
            profile.place = form.cleaned_data["place"]
            profile.languages = form.cleaned_data["language"]
            profile.save()


            print("FORM IS VALId")

            return HttpResponseRedirect(reverse('user:profile_view', args=(kwargs["pk"])))
        else:
            print("FORM IS NOT VALID")
            return render(request, self.template_name, {'form': form, 'pk': kwargs["pk"]})


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

