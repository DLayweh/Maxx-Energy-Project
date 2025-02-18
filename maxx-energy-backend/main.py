from fastapi import FastAPI, Header, HTTPException
import psycopg2
import os
from auth import verify_token  # Import Firebase authentication function


app = FastAPI()

# Database connection
DATABASE_URL = "dbname=maxx_energy user=postgres password=7705894723 host=localhost"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    print("✅ Database connected successfully!")
except Exception as e:
    print("❌ Database connection failed:", e)

@app.get("/public-data")
def get_public_data():
    cursor.execute("SELECT * FROM energy_data ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "plant_name": row[1],
            "location": row[2],
            "energy_generated_kWh": row[3],
            "timestamp": row[4],
        }
        for row in rows
    ]

# Private API Endpoint (Requires Firebase Authentication)
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

# Run the FastAPI server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)