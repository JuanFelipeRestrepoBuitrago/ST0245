import dijkstra as d
import pandas as pd
import draw
import math
import time

coordinates = {
    "Universidad EAFIT": (6.20020215, -75.5784848084993),
    "Universidad Nacional": (6.2623722, -75.5782274),
    "Universidad de Antioquia": (6.268433089452519, -75.56881234818871),
    "Universidad de Medellín": (6.231640688146965, -75.61005360517099),
    "Alcaldía de Medellín": (6.245199939323498, -75.57369230277732),
    "Universidad Pontificia Bolivariana": (6.242522650239001, -75.58939231551759)
}


def distance(point1, point2):
    earth_radius = 6371

    lat1, lon1 = map(math.radians, point1)
    lat2, lon2 = map(math.radians, point2)

    latitudes_difference = math.radians(point2[0] - point1[0])
    longitudes_difference = math.radians(point2[1] - point1[1])

    a = (math.sin(latitudes_difference / 2) ** 2) + (math.cos(lat1) * math.cos(
        lat2) * (math.sin(longitudes_difference / 2) ** 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return earth_radius * c


def find_nearest_coordinate(point, graph):
    min_distance = float("inf")
    nearest_coordinate = None

    for coordinate in graph:
        dist = distance(point, coordinate)
        if dist < min_distance:
            min_distance = dist
            nearest_coordinate = coordinate

    return nearest_coordinate




def generate_graph():
    # Read the data from the csv file and store it in a pandas dataframe
    data = pd.read_csv("calles_de_medellin_con_acoso.csv", sep=";")

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


def test_1():
    graph = generate_graph()

    print("Shortest Path From a Starting Point to a Destination")
    path, distance, risk = d.shortest_path(graph, list(graph.keys())[0], list(graph.keys())[142])
    print("Distance:", str(round(distance, 2)), "\nHarassment Risk:", str(round(risk / (len(path) - 1), 2)))

    print("Safest Path From a Starting Point to a Destination")
    path1, distance1, risk1 = d.safest_path(graph, list(graph.keys())[0], list(graph.keys())[142])
    print("Distance:", str(round(distance1, 2)), "\nHarassment Risk:", str(round(risk1 / (len(path1) - 1), 2)))

    print("Safe and Short Path From a Starting Point to a Destination")
    path2, distance2, risk2 = d.safe_short_path(graph, list(graph.keys())[0], list(graph.keys())[142])
    print("Distance:", str(round(distance2, 2)), "\nHarassment Risk:", str(round(risk2 / (len(path2) - 1), 2)))

    print("Generating map...")
    draw.generate_and_save_map(path, path1, path2)
    print("Map generated!")


# In this test, we are going to find 3 paths to get from Universidad EAFIT to Universidad Nacional.
def test_2():
    graph = generate_graph()
    start, end = find_nearest_coordinate(coordinates["Universidad EAFIT"], graph), find_nearest_coordinate(
        coordinates["Universidad Nacional"], graph)
    total_time = 0

    print(start in graph)
    print(end in graph)
    # time
    # print("Shortest Path From Universidad EAFIT to Universidad Nacional")
    # path, distance, risk = d.shortest_path(graph, start, end)
    # print("Distance:", str(round(distance, 2)), "\nHarassment Risk:", str(round(risk / (len(path) - 1), 2)))


