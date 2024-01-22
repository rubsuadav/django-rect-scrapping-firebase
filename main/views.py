from django.http import JsonResponse
from firebase import firestore
from google.cloud.firestore_v1 import Query


def index(request):
    restaurante_col = firestore.collection(u'restaurantes')
    restaurantes = firestore.collection(u'restaurantes').order_by(
        u'nombre', direction=Query.ASCENDING).limit(30).stream()

    restaurantes_con_comentarios = []
    for restaurante in restaurantes:
        res = restaurante.to_dict()
        comentarios = restaurante_col.document(restaurante.id).collection(
            u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
        res['comentarios'] = [comentario.to_dict()
                              for comentario in comentarios]
        restaurantes_con_comentarios.append(res)
    return JsonResponse(restaurantes_con_comentarios, safe=False)
