

from django.contrib import admin

from .models import Language


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_variant')


admin.site.register(Language, LanguageAdmin)
