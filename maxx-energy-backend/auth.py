import firebase_admin
from firebase_admin import credentials, auth
import json
import os

# Load Firebase credentials from environment variable
firebase_creds = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_creds:
    raise ValueError("FIREBASE_CREDENTIALS environment variable is not set")

# Convert JSON string to dictionary
firebase_creds_dict = json.loads(firebase_creds)

# Initialize Firebase with credentials from environment variable
cred = credentials.Certificate(firebase_creds_dict)
firebase_admin.initialize_app(cred)
