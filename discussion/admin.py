

from django.contrib import admin

from .models import Discussion, Comment, Suggestion, Vote


admin.site.register(Discussion)
admin.site.register(Comment)
admin.site.register(Suggestion)
admin.site.register(Vote)
