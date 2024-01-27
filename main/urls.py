from django.urls import path, include
from .views import IndexView, SubscriptionView, ChatView

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('api/restaurants/<str:restaurant_id>/', IndexView.as_view()),
    path('api/restaurants/', IndexView.as_view()),
    path("api/suscriptions/", SubscriptionView.as_view()),
    path("api/chat/", ChatView.as_view()),
]
