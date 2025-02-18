from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from auth import verify_token
from user_auth import register_user
from visualization import generate_energy_trend_chart

app = FastAPI()

class RegisterRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TwoFARequest(BaseModel):
    otp_code: str

@app.get("/energy-visualization", response_class=HTMLResponse)
def energy_visualization():
   
    try:
       
        mock_rows = [
            (1, "Solar Plant A", "California", 12345.67, "2025-02-10 08:30:00"),
            (2, "Solar Plant B", "Nevada", 9876.54, "2025-02-10 09:00:00"),
            (3, "Solar Plant C", "Arizona", 5678.90, "2025-02-10 09:30:00"),
            (4, "Solar Plant D", "Texas", 15678.32, "2025-02-10 10:00:00"),
            (5, "Solar Plant E", "Florida", 11234.56, "2025-02-10 10:30:00"),
        ]
        chart_html = generate_energy_trend_chart(mock_rows)
        return HTMLResponse(content=chart_html, status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error Generating Visualization: {e}</h3>", status_code=500)



@app.get("/mock-public-data")
def get_mock_public_data():
    
    mock_data = [
        {"id": 1, "plant_name": "Solar Plant A", "location": "California", "energy_generated_kWh": 12345.67, "timestamp": "2025-02-10 08:30:00"},
        {"id": 2, "plant_name": "Solar Plant B", "location": "Nevada", "energy_generated_kWh": 9876.54, "timestamp": "2025-02-10 09:00:00"},
        {"id": 3, "plant_name": "Solar Plant C", "location": "Arizona", "energy_generated_kWh": 5678.90, "timestamp": "2025-02-10 09:30:00"},
        {"id": 4, "plant_name": "Solar Plant D", "location": "Texas", "energy_generated_kWh": 15678.32, "timestamp": "2025-02-10 10:00:00"},
        {"id": 5, "plant_name": "Solar Plant E", "location": "Florida", "energy_generated_kWh": 11234.56, "timestamp": "2025-02-10 10:30:00"},
    ]
    return mock_data

@app.get("/private-data")
def get_private_data(authorization: str = Header(None)):
    
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token = authorization.replace("Bearer ", "")
    user_data = verify_token(token)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return {
        "message": "Private energy data accessed!",
        "user": user_data["email"],
    }

@app.post("/register")
def register_user_api(request: RegisterRequest):

    try:
        result = register_user(request.email, request.password)
        return {"message": "User registered successfully", "user": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login_user_api(request: LoginRequest):
    try:
        
        return {"message": "Login successful (2FA required)", "next_step": "/request-2fa"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/request-2fa")
def request_2fa(authorization: str = Header(None)):
    """Step 1: Send OTP for Two-Factor Authentication."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    user_data = verify_token(authorization.replace("Bearer ", ""))
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user_id = user_data["uid"]
    otp = "123456"  # Mock OTP for presentation
    print(f"📧 Sent OTP to user {user_id}: {otp}")
    return {"message": "2FA code sent to your email (mocked for demo)"}

@app.post("/verify-2fa")
def verify_2fa(request: TwoFARequest):
    """Step 2: Verify the 2FA OTP."""
    if request.otp_code == "123456":  # Mock OTP verification
        return {"message": "2FA verification successful", "status": "approved"}
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")


@app.get("/", tags=["Info"])
def root():
    return {
        "message": "Welcome to MAXX Energy API",
        "docs": "/docs",
        "visualization": "/energy-visualization",
        "mock_public_data": "/mock-public-data",
        "2fa_workflow": {
            "1. Register": "/register",
            "2. Login": "/login",
            "3. Request 2FA": "/request-2fa",
            "4. Verify 2FA": "/verify-2fa"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
