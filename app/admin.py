

from django.contrib import admin

from .models import Profile, UserLanguage
from .models import Discussion, Comment, Suggestion, Vote


admin.site.register(Profile)
admin.site.register(UserLanguage)
admin.site.register(Discussion)
admin.site.register(Comment)
admin.site.register(Suggestion)
admin.site.register(Vote)
