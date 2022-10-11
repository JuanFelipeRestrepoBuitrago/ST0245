import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
from shapely import wkt
import Entrega_2.dijkstra as d


def generate_graph():
    # Read the data from the csv file and store it in a pandas dataframe
    data = pd.read_csv("Entrega_2/calles_de_medellin_con_acoso.csv", sep=";")

    data.harassmentRisk.fillna(data.harassmentRisk.mean(), inplace=True)

    # Create the graph as a dictionary of dictionaries.
    # The keys of the first dictionary are the origin and
    # destination from our dataframe because they both are
    # points of the graph, where we can go or go back.
    graph = {}

    # Iterate over the origin and destination columns
    # of the dataframe and add them to the graph if they
    # are not already there.

    for i in data.index:
        origin = tuple(data["origin"][i][1:-1].split(","))
        destination = tuple(data["destination"][i][1:-1].split(","))

        origin = (float(origin[1]), float(origin[0]))
        destination = (float(destination[1]), float(destination[0]))
        weight = (data["length"][i], data["harassmentRisk"][i], (
                (data["length"][i] + data["harassmentRisk"][i]) / 2
            ))

        if origin not in graph:
            graph[origin] = {}
        # Add the adjacent street of each dictionary in the graph.
        graph[origin][destination] = weight

        if data["oneway"][i]:
            if destination not in graph:
                graph[destination] = {}
            # Add the adjacent street of each dictionary in the graph.
            graph[destination][origin] = weight

    return graph


def get_lat_lon(path):
    lats = []
    lons = []

    for i in path:
        lats.append(i[0])
        lons.append(i[1])

    return lats, lons


# load data
graph = generate_graph()
path, distance, risk = d.shortest_path(graph, list(graph.keys())[0], list(graph.keys())[142])

area = pd.read_csv('Entrega_2/poligono_de_medellin.csv', sep=';')
area['geometry'] = area['geometry'].apply(wkt.loads)
area = gpd.GeoDataFrame(area)

fig = px.choropleth_mapbox(
    area,
    geojson=area.geometry,
    locations=area.index,
    mapbox_style="carto-darkmatter",
    zoom=10,
    center={"lat": float(area.lat), "lon": float(area.lon)},
    opacity=0.5,
)

latitude, longitude = get_lat_lon(path)

fig.add_trace(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode="markers+lines",
        marker={"size": 1},
        line={"width": 4, "color": "red"},
        name="shortest",
        showlegend=True,
        text="This is the shortest path"
))

path, distance, risk = d.safest_path(graph, list(graph.keys())[0], list(graph.keys())[142])

latitude, longitude = get_lat_lon(path)

fig.add_trace(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode="markers+lines",
        marker={"size": 1},
        line={"width": 4, "color": "blue"},
        name="safest",
        showlegend=True,
        text="This is the safest path"
))

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

fig.write_html("Entrega_2/map.html", auto_open=True)


def generate_paths(path: list, name: str, fig):
    latitude, longitude = get_lat_lon(path)

    fig.add_trace(go.Scattermapbox(
        lat=latitude,
        lon=longitude,
        mode="markers+lines",
        marker={"size": 1},
        line={"width": 4, "color": "red"},
        name=name
    ))


def generate_and_save_map(shortest: list=None, safest: list=None, safe_short: list=None):
    # load data
    area = pd.read_csv('Entrega_2/poligono_de_medellin.csv', sep=';')
    area['geometry'] = area['geometry'].apply(wkt.loads)
    area = gpd.GeoDataFrame(area)

    # Create the Medellin map
    fig = px.choropleth_mapbox(
        area,
        geojson=area.geometry,
        locations=area.index,
        mapbox_style="carto-darkmatter",
        zoom=10,
        center={"lat": float(area.lat), "lon": float(area.lon)},
        opacity=0.5,
    )

    # Add the paths to the map
    if shortest is not None:
        generate_paths(shortest, "Shortest", fig)
    if safest is not None:
        generate_paths(safest, "Safest", fig)
    if safe_short is not None:
        generate_paths(safe_short, "Safe and Short", fig)

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    fig.write_html("Entrega_2/map.html", auto_open=True)

