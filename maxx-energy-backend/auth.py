# auth.py
import firebase_admin
from firebase_admin import credentials, auth
import json
import os

# Load Firebase credentials from environment variable
firebase_creds = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_creds:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set")

firebase_creds_dict = json.loads(firebase_creds)
cred = credentials.Certificate(firebase_creds_dict)
firebase_admin.initialize_app(cred)

def verify_token(token):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        return None
