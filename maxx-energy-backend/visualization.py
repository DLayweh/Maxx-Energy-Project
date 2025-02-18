# visualization.py

import plotly.express as px
import pandas as pd
from fastapi.responses import HTMLResponse

def generate_energy_trend_chart(data):
    # Convert data to a DataFrame
    df = pd.DataFrame(data, columns=["id", "plant_name", "location", "energy_generated_kWh", "timestamp"])
    
    # Create a line chart
    fig = px.line(
        df, 
        x="timestamp", 
        y="energy_generated_kWh", 
        color="plant_name",
        title="Energy Generation Trends",
        markers=True
    )
    
    # Return chart as HTML
    return fig.to_html(full_html=False)
