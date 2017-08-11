

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from word.models import Word, WordVersion


# auth
class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:group-detail")

    class Meta:
        model = Group
        fields = ('url', 'name')


# word

class WordVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:wordversion-detail"
    )

    class Meta:
        model = WordVersion
        fields = ('url', 'name', 'link', 'creation_date')


class WordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:word-detail")
    version = WordVersionSerializer()

    class Meta:
        model = Word
        fields = (
            'url', 'word', 'version', 'creation_date', 'wiktionary_link'
        )
