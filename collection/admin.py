

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Collection, CollectionType


class CollectionAdmin(SimpleHistoryAdmin):
    list_display = ('title', 'author', 'reporter', 'type')
    list_filter = ('type',)


admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionType)
