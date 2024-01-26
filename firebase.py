import pyrebase
import firebase_admin
from google.cloud.firestore_v1 import Client as FirestoreClient
import base64
from firebase_admin import credentials
try:
    from local_settings import FIREBASE_API_KEY, FIREBASE_AUTH_DOMAIN, FIREBASE_PROJECT_ID, FIREBASE_STORAGE_BUCKET, FIREBASE_MESSAGING_SENDER_ID, FIREBASE_APP_ID, GOOGLE_APPLICATION_CREDENTIALS_BASE64
except NameError:
    pass

# Firebase configuration
config = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": FIREBASE_AUTH_DOMAIN,
    "projectId": FIREBASE_PROJECT_ID,
    "storageBucket": FIREBASE_STORAGE_BUCKET,
    "messagingSenderId": FIREBASE_MESSAGING_SENDER_ID,
    "appId": FIREBASE_APP_ID,
    "databaseURL": "",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)

# Initialize Firebase Authentication
auth = firebase.auth()

# Initialize Firebase Storage
storage = firebase.storage()

# Initialize Firebase only if it's not already initialized
credentials_base64 = GOOGLE_APPLICATION_CREDENTIALS_BASE64
credentials_bytes = base64.b64decode(credentials_base64)
with open('credentials.json', 'wb') as temp_file:
    temp_file.write(credentials_bytes)
cred = credentials.Certificate('credentials.json')

if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)

# Initialize Firebase Firestore
firestore = FirestoreClient.from_service_account_json('credentials.json')
