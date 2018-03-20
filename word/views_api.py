from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from .models import Word

from rest_framework.decorators import api_view, authentication_classes, permission_classes


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def similar_words(request):
    if request.GET:
        base_word = request.GET.get("word")
        list_of_words = list(Word.objects.all().values_list("word", flat=True))
        # fuzzywuzzy: Get a list of matches ordered by score, the top 3
        results = process.extract(base_word, list_of_words)[0:3]
        similar_words_found = [x[0] for x in results]
        response = {"similar_words_found": similar_words_found}
        return JsonResponse(response)
    else:
        response = {"error": "do GET request"}
        return JsonResponse(response)