

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Tag, ForeignWord, BavarianWord, Description, Translation


admin.site.register(Tag)
admin.site.register(ForeignWord, SimpleHistoryAdmin)
admin.site.register(BavarianWord, SimpleHistoryAdmin)
admin.site.register(Description)
admin.site.register(Translation)
