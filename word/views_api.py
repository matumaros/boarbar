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
        if base_word:
            list_of_words = list(Word.objects.all().values_list("word", flat=True))
            # fuzzywuzzy: Get a list of matches ordered by score, the top 3
            results = process.extract(base_word, list_of_words)[0:3]
            list_of_similar_words = [x[0] for x in results]
            words_and_ids = []

            for word in list_of_similar_words:
                word_obj = Word.objects.filter(word=word).first()
                word_dict = {"word": word, "id": word_obj.id}
                words_and_ids.append(word_dict)

            response = {"similar_words_found": words_and_ids}
            return JsonResponse(response)
        else:
            return JsonResponse({})
    else:
        response = {"error": "do GET request"}
        return JsonResponse(response)
