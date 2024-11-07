# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:25:02 2024

@author: vanleene
"""
# Pour la carte des ports
from flask import Flask, render_template, request
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
import xyzservices 
import requests
# import json # si veux faire de beaux json

app = Flask(__name__)

global all_data 

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/map_template')
def have_a_map():
    country = request.args.get("pays")
    print("parametre lu")
    print(country)
    if country != None:
        # Filtrer le dataframe sur le pays
        ports_filt = ports[ports.state_1789_fr == country]
    m = create_map_port(country)
    return render_template('arctox.html', msg=m.get_root()._repr_html_())

def create_map_port(param):
    ports_filt = ports
    if param != None:
        # Filtrer le dataframe sur le pays
        ports_filt = ports[ports.state_1789_fr == param]
        
    # Calculer le centre de la carte
    if (not ports_filt.empty) and (param != None):
        print('Not empty')
        long = pd.to_numeric(ports_filt['x'], errors='coerce')
        lat = pd.to_numeric(ports_filt['y'], errors='coerce')
        avg_long = np.nanmean(long)
        avg_lat = np.nanmean(lat)
    else:
        # Coordonnées par défaut si aucun port n'est trouvé pour le pays
        avg_lat, avg_lon = 46.166667, -1.150000
        
    # map_ports = folium.Map(location=(ports_filt['y'].iloc[0], ports_filt['x'].iloc[0]),zoom_start=5)
    map_ports = folium.Map(location=(avg_lat, avg_long),zoom_start=5)
    
    group_1 = folium.FeatureGroup("ports").add_to(map_ports)
    # marker_cluster = MarkerCluster().add_to(group_1)
    
    for (index, row) in ports_filt.iterrows():
        folium.Marker(
            location=[row['y'], row['x']],
            tooltip=row["toponym"],
            popup=row["admiralty"],
            icon=folium.Icon(color="blue"),
        ).add_to(group_1)
    folium.LayerControl().add_to(map_ports)
    return map_ports

def get_data_port():
    r = requests.get('http://data.portic.fr/api/ports/?param=&shortenfields=false&both_to=false&date=1787', auth=('user', 'pass'))
    df = pd.DataFrame(r.json())
    return df

if __name__ == '__main__':
    ports = get_data_port()
    app.run(port=5050) 

# pour avoir que les ports de France : http://127.0.0.1:5050/map_template?pays=France
