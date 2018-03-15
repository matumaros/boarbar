
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, UserLanguage

    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'user', 'is_moderator')
    list_filter = ('is_moderator',)

    class Meta:
        model = UserLanguage
        

admin.site.register(Profile)
admin.site.register(UserLanguage, UserLanguageAdmin)
