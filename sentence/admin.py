

from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from .models import Sentence, Translation


admin.site.register(Sentence, SimpleHistoryAdmin)
admin.site.register(Translation, SimpleHistoryAdmin)
