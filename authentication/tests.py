from rest_framework.test import APITestCase
from rest_framework import status
import json
from firebase import auth, firestore


def get_token(self):
    response = self.client.post('/api/auth/login/', data=json.dumps({
        "email": "test@gmail.com",
        "password": "@Test1234"
    }), content_type='application/json')
    return response.data.get('access_token')


def delete_data_user(self):
    token = get_token(self)
    user = auth.get_account_info(token)
    firestore.document(u'customers',
                       user["users"][0]["localId"]).delete()
    auth.delete_user_account(token)


# REGISTER TEST CASES #
class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.url = '/api/auth/'

    # METHOD TO TEST REGISTER NEGATIVE CASES
    def register_invalid_argument(self, data):
        response = self.client.post(
            f'{self.url}register/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## TESTS NEGATIVE CASES ##
    def test_register_invalid_name(self):
        self.register_invalid_argument({
            "name": "T",
            "last_name": "Test",
            "phone": "+34628074492",
            "email": "test@gmail.com",
            "password": "@Test1234"
        })

    def test_register_invalid_last_name(self):
        self.register_invalid_argument({
            "name": "Test",
            "last_name": "T",
            "phone": "+34628074492",
            "email": "test@gmail.com",
            "password": "@Test1234"
        })

    def test_register_invalid_email(self):
        self.register_invalid_argument({
            "name": "Test",
            "last_name": "Test",
            "phone": "+34628074492",
            "email": "d",
            "password": "@Test1234"
        })

    def test_register_invalid_phone(self):
        self.register_invalid_argument({
            "name": "Test",
            "last_name": "Test",
            "phone": "+3462807449",
            "email": "test@gmail.com",
            "password": "@Test1234"
        })

    def test_register_phone_already_exists(self):
        self.register_invalid_argument({
            "name": "Test",
            "last_name": "Test",
            "phone": "+34628074491",
            "email": "test@gmail.com",
            "password": "@Test1234"
        })

    def test_register_invalid_password(self):
        self.register_invalid_argument({
            "name": "Test",
            "last_name": "Test",
            "phone": "+34628074492",
            "email": "test@gmail.com",
            "password": "1234"
        })

    def test_register_user_already_exists(self):
        response = self.client.post(
            f'{self.url}register/', data=json.dumps({
                "name": "Test",
                "last_name": "Test",
                "phone": "+34628074492",
                "email": "rubsuadav@alum.us.es",
                "password": "@Test1234"
            }), content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)

    ## TEST POSITIVE CASES ##
    def test_register_success(self):
        response = self.client.post(f'{self.url}register/', data=json.dumps({
            "name": "Test",
            "last_name": "Test",
            "phone": "+34628074492",
            "email": "test@gmail.com",
            "password": "@Test1234"
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        delete_data_user(self)


# LOGIN TEST CASES #
class LoginViewTestCase(APITestCase):
    def setUp(self):
        self.url = '/api/auth/'

    # METHOD TO TEST LOGIN NEGATIVE CASES
    def login_invalid_argument(self, data):
        response = self.client.post(
            f'{self.url}login/', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    ## TESTS NEGATIVE CASES ##
    def test_login_invalid_email(self):
        self.login_invalid_argument({
            "email": "d",
            "password": "@Test1234"
        })

    def test_login_invalid_password(self):
        self.login_invalid_argument({
            "email": "test@gmail.com",
            "password": "1234"
        })

    def test_login_invalid_user(self):
        response = self.client.post(
            f'{self.url}login/', data=json.dumps({
                "email": "test@gmail.com",
                "password": "@Test1234"
            }), content_type='application/json')
        self.assertEqual(response.status_code,
                         status.HTTP_500_INTERNAL_SERVER_ERROR)
