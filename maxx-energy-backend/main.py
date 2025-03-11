import os
import psycopg2
import jwt
import datetime
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from auth import verify_token  # Firebase authentication
from visualization import generate_energy_trend_chart

# Environment Variables
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
DATABASE_URL = os.getenv("DATABASE_URL", "your_database_url")

app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

script_dir = os.path.dirname(__file__)
static_path = os.path.join(script_dir, "static")

app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

# Mount the static folder to serve HTML, CSS, and JS files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Database Connection
try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed:", e)

# Function to Create JWT Token
def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login Endpoint (Mock Authentication)
@app.post("/login")
def login(username: str, password: str):
    if username == "admin" and password == "password123":
        token = create_access_token(data={"sub": username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# Public Data Endpoint (Fetch Energy Data from Database)
@app.get("/public-data")
def get_public_data():
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
        return {"error": f"Database query failed: {e}"}

# Mock Public Data (For Testing)
@app.get("/mock-public-data")
def get_mock_public_data():
    mock_data = [
        {"id": 1, "plant_name": "Solar Plant A", "location": "California", "energy_generated_kWh": 12345.67, "timestamp": "2025-02-10 08:30:00"},
        {"id": 2, "plant_name": "Solar Plant B", "location": "Nevada", "energy_generated_kWh": 9876.54, "timestamp": "2025-02-10 09:00:00"},
        {"id": 3, "plant_name": "Solar Plant C", "location": "Arizona", "energy_generated_kWh": 5678.90, "timestamp": "2025-02-10 09:30:00"},
        {"id": 4, "plant_name": "Solar Plant D", "location": "Texas", "energy_generated_kWh": 15678.32, "timestamp": "2025-02-10 10:00:00"},
    ]
    return mock_data

# Private Data Endpoint (Requires Authentication)
@app.get("/private-data")
def get_private_data(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.replace("Bearer ", "")
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return {"message": "Private energy data accessed!", "user": user_data["email"]}

# Energy Data Visualization Endpoint
@app.get("/energy-visualization", response_class=HTMLResponse)
def energy_visualization():
    return HTMLResponse(content=generate_energy_trend_chart(), status_code=200)

# Root route (API status)
@app.get("/", response_class=HTMLResponse)
def home():
    return (
        "<h1>Welcome to Maxx Energy API</h1>"
        "<p>Endpoints Available:</p>"
        "<ul>"
        "<li><a href='/docs'>API Documentation</a></li>"
        "<li><a href='/energy-visualization'>Energy Visualization</a></li>"
        "</ul>"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
