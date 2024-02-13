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
    # SEARCH METHODS #
    def test_search_restaurant(self):
        response = self.client.get(
            '/api/restaurants/search/?search=Pasteleria Baklava')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_restaurant_not_found(self):
        response = self.client.get('/api/restaurants/search/?search=McDonalds')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # GET ALL TEST METHODS #
    def test_get_restaurants_without_pagination(self):
        response = self.client.get('/api/restaurants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurants_with_pagination(self):
        response = self.client.get('/api/restaurants/?page=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_with_negative_page(self):
        response = self.client.get('/api/restaurants/?page=-1')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_restaurant_with_invalid_page(self):
        response = self.client.get('/api/restaurants/?page=invalid')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # GET BY ID TEST METHODS #
    def test_get_restaurant_by_id(self):
        response = self.client.get('/api/restaurants/0zxbSBOeNfgt75GbSLfH/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_restaurant_by_id_not_found(self):
        response = self.client.get('/api/restaurants/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
