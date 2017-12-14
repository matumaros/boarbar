

from user.models import UserLanguage
from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    message = "Not a moderator of this language."

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            return True
        try:
            result = obj.version.language.user_languages.get(user=user.profile).is_moderator
        except AttributeError:
            result = True
        except UserLanguage.DoesNotExist:
            result = False

        return result