

from django.views.generic import DetailView

from .models import Profile


class ProfileView(DetailView):
    template_name = 'user/profile.html'
    http_method_name = ['get']
    model = Profile
