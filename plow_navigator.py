import pandas as pd
import requests
import folium
import datetime
from folium.plugins import LocateControl, MarkerCluster, HeatMap
import random

# --- CONFIGURATION ---
# NYC Open Data Socrata IDs
ROUTE_DATA_ID = "sh4i-rsb8" 
LIVE_STATUS_ID = "rmhc-afj9" 
MOCK_MODE = True 

def fetch_nyc_data(dataset_id, limit=5000):
    url = f"https://data.cityofnewyork.us/resource/{dataset_id}.json?$limit={limit}"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        return pd.DataFrame()
    except:
        return pd.DataFrame()

def get_color(last_visit_time):
    if not isinstance(last_visit_time, datetime.datetime): return '#808080'
    hours_ago = (datetime.datetime.now() - last_visit_time).total_seconds() / 3600
    if hours_ago < 1: return '#00FF00'
    elif hours_ago < 3: return '#FFA500'
    else: return '#FF0000'

def main():
    print("NYC PLOW NAVIGATOR")
    df_routes = fetch_nyc_data(ROUTE_DATA_ID, limit=2000)
    if df_routes.empty: return
    
    current_time = datetime.datetime.now()
    df_routes['last_visit'] = df_routes.apply(lambda x: current_time - datetime.timedelta(hours=random.choice([0.5, 2, 6])), axis=1)
    
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12, tiles='CartoDB dark_matter')
    for _, row in df_routes.iterrows():
        geom = row.get('the_geom', row.get('line'))
        if geom and isinstance(geom, dict):
            coords = [[p[1], p[0]] for p in (geom['coordinates'] if geom['type']=='LineString' else geom['coordinates'][0])]
            folium.PolyLine(coords, color=get_color(row['last_visit']), weight=4).add_to(m)
    
    m.save("nyc_plow_mvp.html")
    print("Map generated: nyc_plow_mvp.html")

if __name__ == "__main__":
    main()
