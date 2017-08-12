

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from language.models import Language
from word.models import Word, WordVersion
from user.models import Profile


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


# language
class LanguageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:language-detail"
    )

    class Meta:
        model = Language
        fields = ('url', 'name')


# word
class WordVersionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:wordversion-detail"
    )
    language = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(),
    )

    class Meta:
        model = WordVersion
        fields = ('url', 'name', 'link', 'language', 'creation_date')


class WordSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:word-detail")
    version = serializers.PrimaryKeyRelatedField(
        queryset=WordVersion.objects.all(),
    )
    submitter = serializers.PrimaryKeyRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
    )


    class Meta:
        model = Word
        fields = (
            'url', 'word', 'ipa', 'creation_date', 'wiktionary_link',
            'version', 'status', 'submitter',
        )

    def create(self, validated_data):
        submitter = validated_data['submitter'].profile
        validated_data['submitter'] = submitter
        return Word.objects.create(**validated_data)
