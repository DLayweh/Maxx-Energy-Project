import os
import jwt
import datetime
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse
from auth import verify_token  # Firebase authentication
from visualization import generate_energy_trend_chart


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

app = FastAPI()


def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=30)):
    
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(username: str, password: str):
    
    if username == "admin" and password == "password123":
        token = create_access_token(data={"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

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
from pydantic import BaseModel


MOCK_USER = {
    "email": "demo@maxxenergy.com",
    "password": "password123" 
}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/mock-login")
def mock_login(request: LoginRequest):
    if request.email == MOCK_USER["email"] and request.password == MOCK_USER["password"]:
        return {
            "message": "Login successful",
            "token": "mocked-jwt-token-12345"
        }
    raise HTTPException(status_code=401, detail="Invalid email or password")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/public-data")
def get_public_data():
    """Fetch recent public energy data from the database."""
    try:
        cursor.execute("SELECT id, plant_name, location, energy_generated_kWh, timestamp FROM energy_data ORDER BY timestamp DESC LIMIT 10;")
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "plant_name": row[1],
                "location": row[2],
                "energy_generated_kWh": row[3],
                "timestamp": row[4]
            }
            for row in rows
        ]
    except Exception as e:
        return {"error": f"Failed to fetch public data: {e}"}
