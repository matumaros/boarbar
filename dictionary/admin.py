

from django.contrib import admin

from .models import Tag, Language, Word


admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Word)
