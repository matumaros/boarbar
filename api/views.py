

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from language.models import Language
from word.models import Word, WordVersion


# auth
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


# language
class LanguageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows languages to be viewed or edited.
    """
    queryset = Language.objects.all()
    serializer_class = serializers.LanguageSerializer


# word
class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = serializers.WordSerializer

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)


class WordVersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wordversions to be viewed or edited.
    """
    queryset = WordVersion.objects.all()
    serializer_class = serializers.WordVersionSerializer


@api_view(['GET'])
def user_by_token(request):
    user = request._user
    return Response({'email': user.email})