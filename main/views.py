from django.http import HttpResponse
from .scrapping import PopulateDatabase


def index(request):
    populator = PopulateDatabase()
    populator.populate()
    return HttpResponse("Hello, world. You're at the polls index.")
