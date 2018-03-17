
from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile, UserLanguage

    
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ('language', 'proficiency', 'user', 'is_moderator')
    list_filter = ('is_moderator',)

    class Meta:
        model = UserLanguage
        

admin.site.register(UserLanguage, UserLanguageAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'reputation', 'place', 'join_date', 'max_suggest_words_per_day')

    def user_name(self, obj):
        return obj.user.username


admin.site.register(Profile, ProfileAdmin)
