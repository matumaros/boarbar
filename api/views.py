

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from . import serializers

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


# word
class WordViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = Word.objects.all()
    serializer_class = serializers.WordSerializer

class WordVersionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows wordversions to be viewed or edited.
    """
    queryset = WordVersion.objects.all()
    serializer_class = serializers.WordVersionSerializer
