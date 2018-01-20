
from django.contrib import admin

from .models import Profile, UserLanguage

    

class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ["language","user","is_moderator",]
    class Meta:
        model = UserLanguage
        

admin.site.register(Profile)
admin.site.register(UserLanguage,UserLanguageAdmin)
