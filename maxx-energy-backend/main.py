from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
import psycopg2
import os
from auth import verify_token  # Firebase authentication
from visualization import generate_energy_trend_chart

app = FastAPI()

# ✅ Database Connection Setup
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed:", e)
    conn = None
    cursor = None

# ✅ Public Data Endpoint (Fetching Real Data)
@app.get("/public-data")
def get_public_data():
    """Fetches real energy data from PostgreSQL."""
    if not cursor:
        raise HTTPException(status_code=500, detail="Database connection not available")

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
        raise HTTPException(status_code=500, detail=f"Error fetching data: {e}")

# ✅ Energy Visualization (Using Real Data)
@app.get("/energy-visualization", response_class=HTMLResponse)
def energy_visualization():
    """Generates an energy trend visualization from real data."""
    if not cursor:
        return HTMLResponse(content="<h3>Error: Database connection not available</h3>", status_code=500)

    try:
        cursor.execute("SELECT id, plant_name, location, energy_generated_kWh, timestamp FROM energy_data ORDER BY timestamp ASC LIMIT 100;")
        rows = cursor.fetchall()
        chart_html = generate_energy_trend_chart(rows)
        return HTMLResponse(content=chart_html, status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error Generating Visualization: {e}</h3>", status_code=500)

# ✅ Private Data (Requires Authentication)
@app.get("/private-data")
def get_private_data(authorization: str = Header(None)):
    """Returns private energy data only if authenticated."""
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

# ✅ Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
