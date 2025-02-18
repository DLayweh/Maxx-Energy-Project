
from firebase_admin import auth

def register_user(email, password):
   
    try:
        user = auth.create_user(
            email=email,
            password=password,
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise Exception(f"Failed to create user: {e}")

def login_user(email, password):
    raise Exception("Login should be handled on the client-side with Firebase Client SDK.")
