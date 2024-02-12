from django.urls import path, include
from .views import IndexView, SubscriptionView, ChatView, SearchRestaurantsByNameView

urlpatterns = [
    # AUTHENTICATION URLS #
    path('api/auth/', include('authentication.urls')),

    # RESTAURANTS URLS #
    path('api/restaurants/search/', SearchRestaurantsByNameView.as_view()),
    path('api/restaurants/<str:restaurant_id>/', IndexView.as_view()),
    path('api/restaurants/', IndexView.as_view()),

    # SUBSCRIPTIONS URLS #
    path("api/suscriptions/", SubscriptionView.as_view()),

    # CHAT URLS #
    path("api/chat/", ChatView.as_view()),
]
