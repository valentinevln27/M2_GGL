# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 08:25:02 2024

@author: vanleene
"""

from flask import Flask, render_template
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

@app.route('/moi')
def hello_me():
    return 'Hello, Valentine!'
   
@app.route('/alldata') 
def send_alldata():
    # print('Jai lu les données.')
    return all_data.to_json(orient='records')

def read_alldata():
    all_data = pd.read_excel('data for analyses_2010_2011_analyses.xls', 'data for analyses_2010_2011_ana')
    return all_data

@app.route('/hello_template')
def template_test():
    return render_template('hello.html', msg='<br>titi<br>')

@app.route('/test')
def df_to_html():
    test = all_data.to_html()
    return render_template('arctox.html', msg=test)

def read_data_bird():
    bird = gpd.read_file('output.geojson')
    world_land = gpd.read_file('./ne_110m_land/ne_110m_land.shp') # Mapshaper
    return bird, world_land

def create_map_port():
    smithsonian_provider = xyzservices.TileProvider(name="Stamen maps, hosted by Smithsonian",
                                                     url="https://watercolormaps.collection.cooperhewitt.org/tile/watercolor/{z}/{x}/{y}.jpg",
                                                     attribution="(C) Stamen Design")
    map_ports = folium.Map(location=(46.166667, -1.150000), 
                           tiles=smithsonian_provider, 
                           zoom_start=5)
    marker_cluster = MarkerCluster().add_to(map_ports)
    for (index, row) in df.iterrows():
        if row['state_1789_fr'] == 'France':
            folium.Marker(
                location=[row['y'], row['x']],
                tooltip=row["toponym"],
                popup=row["admiralty"],
                icon=folium.Icon(icon='cloud', color="blue"),
            ).add_to(marker_cluster)
        else:
            folium.Marker(
                location=[row['y'], row['x']],
                tooltip=row["toponym"],
                popup=row["admiralty"],
                icon=folium.Icon(icon='cloud', color="green"),
            ).add_to(marker_cluster)
    return map_ports

def get_data_port():
    r = requests.get('http://data.portic.fr/api/ports/?param=&shortenfields=false&both_to=false&date=1787', auth=('user', 'pass'))
    df = pd.DataFrame(r.json())
    return df

# @app.route('/alldata/bird')
# def map_bird():
#     m = bird.plot()
#     return m

if __name__ == '__main__':
    all_data = read_alldata()
    bird, world_land = read_data_bird()
    print('Fichier lu une seule fois')
    app.run(port=5050) 

#%%
# all_data = pd.read_excel(r'data for analyses_2010_2011_analyses.xls', 'data for analyses_2010_2011_ana')
# all_data_json = all_data.to_json(orient='records')

#%% Avec Mapshaper
bird = gpd.read_file('output.geojson')
# bird.plot()
world_land = gpd.read_file('./ne_110m_land/ne_110m_land.shp') # Mapshaper

fig, ax = plt.subplots()
world_land.plot(ax=ax)
bird.plot(ax=ax, column='week', legend=True, markersize=5)

#%%
df = pd.read_csv('C:/cours/master/M2/Environnemental Data to Information/TD_06112024/Kap Hoegh GLS 20102011_sun3_saison.csv')
# df = df.rename([...])
# df = df.drop([...], axis=1)
# gps = gpd.GeoDataFram(df, geometry=gpd.points_from_xy(df.long,df.lat), crs='EPSG:4326')

#%% Pour la carte des oiseaux
from flask import Flask, render_template
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
def df_to_html():
    m = create_map_bird()
    return render_template('arctox.html', msg=m.get_root()._repr_html_())

def read_data_bird():
    bird = gpd.read_file('output.geojson')
    world_land = gpd.read_file('./ne_110m_land/ne_110m_land.shp') # Mapshaper
    return bird, world_land

def create_map_bird():
    fig, ax = plt.subplots()
    world_land.plot(ax=ax)
    bird.plot(ax=ax, column='week', legend=True, markersize=5)
    # fig.save(f'carto_bird.png', 'png')
    # test = all_data.to_html()
    bird_map = bird.to_html
    return bird_map

if __name__ == '__main__':
    bird, world_land = read_data_bird()
    # print('Fichier lu une seule fois')
    app.run(port=5050) 

#%% Pour la carte des ports
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

#%%
import  numpy as np
import numpy as np

# Assurez-vous de convertir 'x' et 'y' en flottants, en remplaçant les valeurs non convertibles par NaN
long = pd.to_numeric(ports['x'], errors='coerce')
lat = pd.to_numeric(ports['y'], errors='coerce')

# Calculez la moyenne en ignorant les NaN
test_m_long = np.nanmean(long)
test_m_lat = np.nanmean(lat)
