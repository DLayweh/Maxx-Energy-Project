from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
import psycopg2
import os
from auth import verify_token  # Firebase authentication
from visualization import generate_energy_trend_chart

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Database connected successfully!")

    
    with open("database_init.sql", "r") as sql_file:
        cursor.execute(sql_file.read())
        conn.commit()
        print("✅ Sample database initialized.")
except Exception as e:
    print("❌ Database connection failed:", e)

@app.get("/energy-visualization", response_class=HTMLResponse)
def energy_visualization():
    try:
        cursor.execute("SELECT id, plant_name, location, energy_generated_kWh, timestamp FROM energy_data ORDER BY timestamp ASC LIMIT 100;")
        rows = cursor.fetchall()
        chart_html = generate_energy_trend_chart(rows)
        return HTMLResponse(content=chart_html, status_code=200)
    except Exception as e:
        return HTMLResponse(content=f"<h3>Error Generating Visualization: {e}</h3>", status_code=500)

@app.get("/public-data")
def get_public_data():
    cursor.execute("SELECT * FROM energy_data ORDER BY timestamp DESC LIMIT 10;")
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


@app.get("/mock-public-data")
def get_mock_public_data():
    mock_data = [
        {"id": 1, "plant_name": "Solar Plant A", "location": "California", "energy_generated_kWh": 12345.67, "timestamp": "2025-02-10 08:30:00"},
        {"id": 2, "plant_name": "Solar Plant B", "location": "Nevada", "energy_generated_kWh": 9876.54, "timestamp": "2025-02-10 09:00:00"},
        {"id": 3, "plant_name": "Solar Plant C", "location": "Arizona", "energy_generated_kWh": 5678.90, "timestamp": "2025-02-10 09:30:00"},
        {"id": 4, "plant_name": "Solar Plant D", "location": "Texas", "energy_generated_kWh": 15678.32, "timestamp": "2025-02-10 10:00:00"},
        {"id": 5, "plant_name": "Solar Plant E", "location": "Florida", "energy_generated_kWh": 11234.56, "timestamp": "2025-02-10 10:30:00"},
        {"id": 6, "plant_name": "Solar Plant F", "location": "New Mexico", "energy_generated_kWh": 13578.44, "timestamp": "2025-02-10 11:00:00"},
        {"id": 7, "plant_name": "Solar Plant G", "location": "Utah", "energy_generated_kWh": 14233.89, "timestamp": "2025-02-10 11:30:00"},
        {"id": 8, "plant_name": "Solar Plant H", "location": "Colorado", "energy_generated_kWh": 12098.78, "timestamp": "2025-02-10 12:00:00"},
        {"id": 9, "plant_name": "Solar Plant I", "location": "Oregon", "energy_generated_kWh": 11345.23, "timestamp": "2025-02-10 12:30:00"},
        {"id": 10, "plant_name": "Solar Plant J", "location": "Washington", "energy_generated_kWh": 10987.65, "timestamp": "2025-02-10 13:00:00"}
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
