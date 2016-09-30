

from django.contrib import admin


from .models import Tag, Word, WordHistory


admin.site.register(Tag)
admin.site.register(Word)
admin.site.register(WordHistory)
