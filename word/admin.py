

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Tag, Word, Description, Translation


admin.site.register(Tag)
admin.site.register(Word, SimpleHistoryAdmin)
admin.site.register(Description)
admin.site.register(Translation, SimpleHistoryAdmin)
