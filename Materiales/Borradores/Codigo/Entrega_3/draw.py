from functools import reduce
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
from shapely import wkt


def get_lat_lon(path):
    lats = []
    lons = []

    for i in path:
        lats.append(i[0])
        lons.append(i[1])

    return lats, lons


def generate_paths(path: list, color: str, name: str, fig):
    latitude, longitude = get_lat_lon(path)

    fig.add_trace(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode="markers+lines",
        marker={"size": 1},
        line={"width": 4, "color": color},
        name=name
    ))


def generate_start_and_end_points(path: list, fig, start_name, end_name):
    latitude, longitude = get_lat_lon(path)

    fig.add_trace(go.Scattermapbox(
        lat=[latitude[0]],
        lon=[longitude[0]],
        mode="markers",
        marker={"size": 13, "color": "black"},
        name=start_name,
        showlegend=True,
        text="This is the Start Point"
    ))

    fig.add_trace(go.Scattermapbox(
        lat=[latitude[-1]],
        lon=[longitude[-1]],
        mode="markers",
        marker={"size": 13, "color": "darkred"},
        name=end_name,
        showlegend=True,
        text="This is the End Point"
    ))


def generate_and_save_map(shortest: list = None, safest: list = None, safe_short: list = None,
                          start_name="Start Point", end_name="End Point"):
    # load data
    area = pd.read_csv('poligono_de_medellin.csv', sep=';')
    area['geometry'] = area['geometry'].apply(wkt.loads)
    area = gpd.GeoDataFrame(area)

    # Create the Medellín map
    fig = px.choropleth_mapbox(
        area,
        geojson=area.geometry,
        locations=area.index,
        mapbox_style="carto-darkmatter",
        zoom=10,
        center={"lat": float(area.lat), "lon": float(area.lon)},
        opacity=0.5,
    )

    generate_start_and_end_points(reduce(lambda x, y: x if len(x) < len(y) else y,
                                         list(filter(lambda x: x is not None, [shortest, safest, safe_short]))), fig,
                                  start_name, end_name)

    # Add the paths to the map
    if shortest is not None:
        generate_paths(shortest, "whitesmoke", "Shortest", fig)
    if safest is not None:
        generate_paths(safest, "aqua", "Safest", fig)
    if safe_short is not None:
        generate_paths(safe_short, "violet", "Safe and Short", fig)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.write_html("map.html", auto_open=True)
