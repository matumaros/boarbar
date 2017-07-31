

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Tag, WordVersion, Word, Description, Translation, Collection
)


admin.site.register(Tag)
admin.site.register(WordVersion)
admin.site.register(Word, SimpleHistoryAdmin)
admin.site.register(Description)
admin.site.register(Translation, SimpleHistoryAdmin)
admin.site.register(Collection, SimpleHistoryAdmin)
