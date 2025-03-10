

import plotly.express as px
import pandas as pd
from fastapi.responses import HTMLResponse

def generate_energy_trend_chart(data):
  
    df = pd.DataFrame(data, columns=["id", "plant_name", "location", "energy_generated_kWh", "timestamp"])
    
   
    fig = px.line(
        df, 
        x="timestamp", 
        y="energy_generated_kWh", 
        color="plant_name",
        title="Energy Generation Trends",
        markers=True
    )
    
    
    return fig.to_html(full_html=False)
