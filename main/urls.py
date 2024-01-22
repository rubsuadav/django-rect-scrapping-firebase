from django.urls import path
from .views import IndexView

urlpatterns = [
    path('api/restaurants/<str:restaurant_id>/', IndexView.as_view()),
    path('api/restaurants/', IndexView.as_view()),
]
