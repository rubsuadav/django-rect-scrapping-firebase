from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from requests.exceptions import HTTPError
import json

# using to implements register and login logic
from firebase import auth, firestore, app

# using to update some parameters of the user
from firebase_admin import auth as auth_admin
from firebase_admin.auth import PhoneNumberAlreadyExistsError
from firebase_admin._auth_client import Client

# local imports
from .validate import validate_register, validate_login


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data

            name = data.get('name')
            last_name = data.get('last_name')
            phone = data.get('phone')
            email = data.get('email')
            password = data.get('password')

            validate_register(name, last_name, phone, email, password)

            user = auth.create_user_with_email_and_password(email, password)
            auth.update_profile(
                user['idToken'], display_name=name + ' ' + last_name)
            try:
                auth_admin.update_user(user['localId'], phone_number=phone)
            except PhoneNumberAlreadyExistsError as e1:
                auth.delete_user_account(user['idToken'])
                firestore.document(u'customers', user['localId']).delete()
                return Response(data={'firebase_error': str(e1)}, status=status.HTTP_400_BAD_REQUEST)
            # created successfully the user with all the data without errors
            return Response(data={'exito': 'usuario creado con éxito'}, status=status.HTTP_201_CREATED)
        except ValidationError as e2:
            return Response(data=e2.detail, status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as e3:
            return Response(data=json.loads(e3.strerror), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data

            email = data.get('email')
            password = data.get('password')

            validate_login(email, password)

            user = auth.sign_in_with_email_and_password(email, password)
            user_details = Client(app).get_user(user['localId'])
            if (not user_details.email_verified):
                auth.send_email_verification(user['idToken'])
            return Response(data={'access_token': user['idToken'], 'refresh_token': user["refreshToken"]}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(data=e.detail, status=status.HTTP_400_BAD_REQUEST)
        except HTTPError as e2:
            return Response(data=json.loads(e2.strerror), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
