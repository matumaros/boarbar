from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user.models import Language, UserLanguage


class SignUpForm(UserCreationForm):
    field_order = (
        'username', 'first_name', 'last_name', 'email', 'description',
        'language', 'proficiency', 'place', 'password1', 'password2'
    )

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    description = forms.CharField(
        max_length=500, required=False, help_text="Tell us a bit about yourself", widget=forms.Textarea
    )
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    place = forms.CharField(max_length=100)
    proficiency = forms.ChoiceField(choices=UserLanguage.PROF,
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    description = forms.CharField(
        max_length=500, required=False, help_text="Tell us a bit about yourself", widget=forms.Textarea
    )
    place = forms.CharField(max_length=100)
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      widget=forms.CheckboxSelectMultiple)
    proficiency = forms.ChoiceField(choices=UserLanguage.PROF)

    class Meta:
        model = User
        fields = ("description", "place", "language", "proficiency")
