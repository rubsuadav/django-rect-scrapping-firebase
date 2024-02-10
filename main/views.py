from firebase import firestore
from google.cloud.firestore_v1 import Query
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def get_restaurant_comments(restaurante_col, restaurantes):
    restaurantes_con_comentarios = []
    for restaurante in restaurantes:
        res = restaurante.to_dict()
        comentarios = restaurante_col.document(restaurante.id).collection(
            u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
        res['comentarios'] = [comentario.to_dict()
                              for comentario in comentarios]
        restaurantes_con_comentarios.append(res)

    return restaurantes_con_comentarios


### RESTAURANTS METHODS ###
class IndexView(APIView):
    def get(self, request, restaurant_id=''):
        page = request.query_params.get('page')
        restaurante_col = firestore.collection(u'restaurantes')
        if restaurant_id == '':  # Listado de restaurantes
            if page:  # Si se especifica la paginacion
                try:
                    page = int(page)
                    if int(page) < 1:  # Si la pagina es menor a 1
                        return Response(data={"error": "Pagina debe de ser mayor o igual a 1"}, status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    return Response(data={"error": "Pagina debe de ser un numero"}, status=status.HTTP_400_BAD_REQUEST)

                # 10 restaurantes por pagina
                restaurantes = restaurante_col.order_by(
                    u'nombre', direction=Query.ASCENDING).limit(10).offset((int(page) - 1) * 10).stream()
                return Response(data=get_restaurant_comments(restaurante_col, restaurantes), status=status.HTTP_200_OK)

            else:  # Sin paginacion
                restaurantes = restaurante_col.order_by(
                    u'nombre', direction=Query.ASCENDING).stream()
                return Response(data=get_restaurant_comments(restaurante_col, restaurantes), status=status.HTTP_200_OK)

        else:  # Detalle de un restaurante
            restaurante = restaurante_col.document(
                str(restaurant_id)).get()
            if restaurante.exists:  # Si existe el restaurante
                res = restaurante.to_dict()
                comentarios = restaurante_col.document(
                    str(restaurant_id)).collection(u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
                res['comentarios'] = [comentario.to_dict()
                                      for comentario in comentarios]
                return Response(data=res, status=status.HTTP_200_OK)
            else:  # Si no existe el restaurante
                return Response(data={'error': 'Restaurante no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class SearchRestaurantsByNameView(APIView):
    def get(self, request):
        query = request.query_params.get('search')
        restaurante_col = firestore.collection(u'restaurantes')
        try:
            restaurantes = restaurante_col.where(
                u'nombre', u'==', query).stream()
            return Response(data=get_restaurant_comments(restaurante_col, restaurantes)[0], status=status.HTTP_200_OK)
        except:
            return Response(data={'error': f'No se ha encontrado el restaurante con el nombre {query}'},
                            status=status.HTTP_404_NOT_FOUND)


## SUBSCRIPTION METHODS ##
class SubscriptionView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        doc_ref = firestore.collection(u'customers', user_id, u'checkout_sessions').add({
            'price': request.data.get('price'),
            "trial_from_plan": True,
            "allow_promotion_codes": True,
            'success_url': 'https://example.com/success',
            'cancel_url': 'https://example.com/cancel',
        })
        doc = doc_ref[1].get()
        while 'url' not in doc.to_dict():
            doc = doc_ref[1].get()
        checkout_session = doc.to_dict()
        return Response(data={"checkout_session": checkout_session["url"]}, status=status.HTTP_200_OK)


## CHAT METHODS ##
class ChatView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        prompt = request.data.get('prompt')
        doc_ref = firestore.collection(u'customers', user_id, u'chats').add({
            'prompt': prompt
        })
        doc = doc_ref[1].get()
        while 'response' not in doc.to_dict():
            doc = doc_ref[1].get()
        response = doc.to_dict()
        return Response(data={"response": response}, status=status.HTTP_200_OK)
