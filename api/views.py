

from difflib import SequenceMatcher

from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from language.models import Language
from word.models import Word, WordVersion, Description
from .permissions import IsModeratorPermission
from . import serializers


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
    permission_classes = (IsModeratorPermission,)

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
    user = request.us
    return Response({'email': user.email})


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def similar_words(request):
    if request.GET:
        base_word = request.GET.get("word")
        default_variant = request.GET.get("language")
        limit = request.GET.get("limit", 3)
        if base_word:
            list_of_words = list(Word.objects.all().filter(
                version__language__default_variant=default_variant))
            most_similar_words = sorted(
                list_of_words,
                key=lambda word: SequenceMatcher(a=base_word, b=word.word).ratio(),
                reverse=True
            )[:limit]

            words_desc_ids = []

            for word in most_similar_words:
                descriptions = word.desc.all().filter(language__default_variant=default_variant)
                if descriptions:
                    desc_obj = descriptions.first()
                    desc_short = desc_obj.short
                else:
                    desc_short = ""

                word_dict = {"word": word.word, "id": word.id, "desc": desc_short}
                words_desc_ids.append(word_dict)

            response = {"similar_words_found": words_desc_ids}
            return JsonResponse(response)
        else:
            return JsonResponse({})
    else:
        response = {"error": "do GET request"}
        return JsonResponse(response)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def word_descriptions(request):
    word_id = request.GET.get("word_id")
    language_str = request.GET.get("language_str")
    word = Word.objects.get(id=word_id)
    descs = word.desc.all().filter(language__id=language_str).values()
    return JsonResponse(list(descs), safe=False)

@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def word_synonyms(request):
    word_id = request.GET.get("word_id")
    language_str = request.GET.get("language_str")
    version = WordVersion.objects.all().filter(language__id=language_str)
    version_values_list = list(version.values())
    version_id = version_values_list[0]["id"]
    word = Word.objects.get(id=word_id)
    syn = word.synonyms.all().filter(version__id=version_id).values()
    return JsonResponse(list(syn), safe=False)