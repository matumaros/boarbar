

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Tag, WordVersion, Word, Description, WordLocation
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class WordVersionAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'link', 'creation_date')
    list_filter = ('language',)


class WordAdmin(SimpleHistoryAdmin):
    list_display = ('word', 'status', 'submitter', 'creation_date', 'version')
    list_filter = ('status', 'version')


class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('short', 'extended', 'language')
    list_filter = ('language',)


class WordLocationAdmin(admin.ModelAdmin):
    list_display = ('word', 'place', 'submitter', 'creation_date')


admin.site.register(Tag, TagAdmin)
admin.site.register(WordVersion, WordVersionAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Description, DescriptionAdmin)
admin.site.register(WordLocation, WordLocationAdmin)
