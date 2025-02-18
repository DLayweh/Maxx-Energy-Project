import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

# Function to verify authentication token
def verify_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # This contains user info like email, UID
    except Exception as e:
        return None
