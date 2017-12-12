

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Collection


admin.site.register(Collection, SimpleHistoryAdmin)
