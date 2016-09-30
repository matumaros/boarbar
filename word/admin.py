

from django.contrib import admin


from .models import Tag, Word, WordHistory, Translation


admin.site.register(Tag)
admin.site.register(Word)
admin.site.register(WordHistory)
admin.site.register(Translation)
