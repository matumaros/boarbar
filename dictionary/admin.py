

from django.contrib import admin

from .models import Tag, Language, Dialect, Word


admin.site.register(Tag)
admin.site.register(Language)
admin.site.register(Dialect)
admin.site.register(Word)
