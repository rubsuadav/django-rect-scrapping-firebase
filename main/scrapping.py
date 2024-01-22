import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from tqdm import tqdm
from colorama import Fore, Style

# local imports
from firebase import firestore

main_url = "https://gastroranking.es"


# Auxiliar methos
def populate_restaurants_details(s3):
    datos = s3.find("section", id="content")
    try:
        detalles = datos.find("div", class_="hl_row")
    except:
        pass

    provincia = datos.find(
        "h1", class_="contentTitle").find_all("span")[1].text.strip()

    calle = detalles.a.address.find_all(
        "span")[0].text.strip()

    try:
        telefono = detalles.find(
            "a", class_="i-block phone").text.strip().replace("+34", "")
    except:
        telefono = None

    try:
        web = detalles.find("div", class_="pull-right").a["href"]
    except:
        web = None

    descripcion = []
    try:
        descripciones = s3.find(
            "section", class_="container premiumInfo").find("div", class_="tab-content").find_all("p")
        for d in descripciones:
            desc = d.text.strip()
            descripcion.append(desc)
        descripcion = '\n\f'.join(descripcion)
    except:
        descripcion = "Sin descripcion"

    return provincia, calle, telefono, web, descripcion


def populate_scores(s3):
    datos_gastroranking = s3.find(
        "section", id="ranking").find("div", class_="ranking")
    datos_plataformas = s3.find("section", class_="container nopadding reviews").find(
        "div", class_="reviewsBySite").find_all("table")

    puntos_gastroranking = float(datos_gastroranking.find(
        "div", class_="globalRanking").text.strip().replace(",", "."))
    numero_opiniones_gastroranking = int(
        datos_gastroranking.p.b.span.text.strip().replace(".", ""))

    numero_opiniones_tripadvisor = 0
    puntos_tripadvisor = 0.
    for dato in datos_plataformas:
        for row in dato.find_all('tr')[1:]:
            celda = row.find('a', class_='sitename').img['title']
            if "Tripadvisor" in celda:
                if row.find('td', class_='rightText') is not None:
                    trivadvisor_row = row.find_next("td", class_="rightText")

                    numero_opiniones_tripadvisor = int(
                        trivadvisor_row.text.strip())
                    puntos_tripadvisor = float(trivadvisor_row.find_next(
                        "td", class_="rightText rating").text.strip().replace(",", "."))
                else:
                    numero_opiniones_tripadvisor = 0
                    puntos_tripadvisor = 0.

    return puntos_gastroranking, puntos_tripadvisor, numero_opiniones_gastroranking, numero_opiniones_tripadvisor


def populate_comments(s3):
    datos_comentarios = s3.find("section", class_="container nopadding reviews").find(
        "div", id="reviews").find_all("div", {"itemprop": "review"})
    lista_comentarios = []
    for dato in datos_comentarios:
        comentario = {}
        comentario['texto'] = dato.find("div", class_="text").text.strip()

        datos_usuario = dato.find(
            "div", class_="userSite pull-left")

        comentario['fecha'] = datos_usuario.find(
            "div", class_="ratingDate").text.strip()
        comentario['usuario'] = datos_usuario.span.text.strip()
        lista_comentarios.append(comentario)

    return lista_comentarios


def populate_restaurants(data_url):
    # lista de restaurantes que se van a guardar en la base de datos de firebase
    restaurantes = []
    # hay 15 por cada pagina y 14781 paginas, es decir, 221715 restaurantes
    # ponemos 550 restaurantes para que no tarde tanto, es decir, 37 paginas
    for i in range(1, 15):
        url = data_url + "?page=" + str(i)
        page = requests.get(url)
        s2 = BeautifulSoup(page.content, "html.parser")

        data = s2.find("section", id="content")
        datos = data.find("div", class_="searchResults").find_all(
            "div", class_="resultItem")

        for dato in datos:
            etiqueta_enlace = dato.h3.a
            nombre = etiqueta_enlace.text.strip()
            enlace = etiqueta_enlace["href"]
            url_restaurante = main_url + enlace

            page2 = requests.get(url_restaurante)
            s3 = BeautifulSoup(page2.content, "html.parser")

            prov, calle, tel, web, desc = populate_restaurants_details(s3)
            ptos_gastro, ptos_trip, op_gastro, op_trip = populate_scores(s3)
            datos_comentario = populate_comments(s3)

            comentarios = []  # lista de comentarios que se van a guardar en la base de datos de firebase

            for dato_comentario in datos_comentario:
                comentarios.append(dato_comentario)

            restaurantes.append({
                "nombre": nombre,
                "provincia": prov,
                "calle": calle,
                "telefono": tel,
                "web": web,
                "descripcion": desc,
                "puntuacion_gastroranking": ptos_gastro,
                "puntuacion_tripadvisor": ptos_trip,
                "opiniones_gastroranking": op_gastro,
                "opiniones_tripadvisor": op_trip,
                "comentarios": comentarios,
            })

    return restaurantes


def scrapping():
    main_page = requests.get(main_url)
    s = BeautifulSoup(main_page.content, "html.parser")
    main_data = s.find(
        "div", class_="container infoContentWrapper").div.div.div
    url = main_data.a["href"]
    data_url = main_url + url
    restaurants = populate_restaurants(data_url)

    return restaurants


# Main method
class PopulateDatabase(BaseCommand):
    help = 'Populate database'

    def populate(self, *args, **options):
        restaurants = scrapping()
        with tqdm(total=len(restaurants), desc='Populating database') as pbar:
            for i, restaurant in enumerate(restaurants):
                comments = restaurant.pop('comentarios', [])
                _, restaurant_ref = firestore.collection(
                    u'restaurantes').add(restaurant)
                for comment in comments:
                    _, _ = restaurant_ref.collection(
                        'comentarios').add(comment)

                pbar.update(1)

                # Calcute % completed
                percent_complete = (i + 1) / len(restaurants) * 100

                # Change the color of the progress bar according to the percentage completed
                if 0 <= percent_complete <= 25:
                    color = Fore.RED
                elif 25 < percent_complete <= 50:
                    color = Fore.YELLOW
                elif 50 < percent_complete <= 75:
                    color = Fore.GREEN
                else:
                    color = Fore.BLUE

                # Update the style of the description bar
                pbar.set_description(
                    f'{color}Populating database{Style.RESET_ALL}')

        self.stdout.write(self.style.SUCCESS(
            '\n Successfully populated database'))
