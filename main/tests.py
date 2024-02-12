from rest_framework.test import APITestCase
from rest_framework import status
import json


def get_token(self):
    response = self.client.post('/api/auth/login/', data=json.dumps({
        "email": "localuser@gmail.com",
        "password": "@Test1234"
    }), content_type='application/json')
    return response.data.get('access_token')


# RESTAURANTS TEST CASES #
class RestaurantsViewTestCase(APITestCase):
    def test_search_restaurant(self):
        response = self.client.get(
            '/api/restaurants/search/?search=Pasteleria Baklava')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_restaurant_not_found(self):
        response = self.client.get('/api/restaurants/search/?search=McDonalds')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
