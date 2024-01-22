from firebase import firestore
from google.cloud.firestore_v1 import Query
from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
    def get(self, request, restaurant_id=''):
        page = request.query_params.get('page')
        restaurante_col = firestore.collection(u'restaurantes')

        # Listado de restaurantes
        if restaurant_id == '':
            if page:  # Si se especifica la paginacion
                try:
                    page = int(page)
                    if int(page) < 1:  # Si la pagina es menor a 1
                        return Response(data={"error": "Pagina debe de ser mayor o igual a 1"}, status=400)
                except Exception:
                    return Response(data={"error": "Pagina debe de ser un numero"}, status=400)

                # 10 restaurantes por pagina
                restaurantes = restaurante_col.order_by(
                    u'nombre', direction=Query.ASCENDING).limit(30).offset((int(page) - 1) * 30).stream()

                restaurantes_con_comentarios = []
                for restaurante in restaurantes:
                    res = restaurante.to_dict()
                    comentarios = restaurante_col.document(restaurante.id).collection(
                        u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
                    res['comentarios'] = [comentario.to_dict()
                                          for comentario in comentarios]
                    restaurantes_con_comentarios.append(res)
                return Response(data=restaurantes_con_comentarios, status=200)

            else:  # Sin paginacion
                restaurantes = restaurante_col.order_by(
                    u'nombre', direction=Query.ASCENDING).stream()
                restaurantes_con_comentarios = []
                for restaurante in restaurantes:
                    res = restaurante.to_dict()
                    comentarios = restaurante_col.document(
                        restaurante.id).collection(u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
                    res['comentarios'] = [comentario.to_dict()
                                          for comentario in comentarios]
                    restaurantes_con_comentarios.append(res)
                return Response(data=restaurantes_con_comentarios, status=200)

        else:  # Detalle de un restaurante
            restaurante = restaurante_col.document(
                str(restaurant_id)).get()
            if restaurante.exists:  # Si existe el restaurante
                res = restaurante.to_dict()
                comentarios = restaurante_col.document(
                    str(restaurant_id)).collection(u'comentarios').order_by(u'fecha', direction=Query.ASCENDING).stream()
                res['comentarios'] = [comentario.to_dict()
                                      for comentario in comentarios]
                return Response(data=res, status=200)
            else:  # Si no existe el restaurante
                return Response(data={'error': 'Restaurante no encontrado'}, status=404)
