

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Tag, WordVersion, Word, Description, WordLocation
)


admin.site.register(Tag)
admin.site.register(WordVersion)
admin.site.register(Word, SimpleHistoryAdmin)
admin.site.register(Description)
admin.site.register(WordLocation)
