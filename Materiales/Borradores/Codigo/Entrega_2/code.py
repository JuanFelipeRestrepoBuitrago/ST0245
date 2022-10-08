import pandas as pd
import math
from collections import deque


# This method finds the vertex of the graph with the lowest distance
# of all vertexes that are in unvisited
def find_the_lowest_distance(unvisited: deque, distances: dict):
    lowest_key = ""
    lowest = math.inf

    for node in unvisited:
        if distances[node][0] < lowest:
            lowest_key = node
            lowest = distances[node][0]

    unvisited.remove(lowest_key)
    return lowest_key


# This method generates the necessary dictionaries to run dijkstra's algorithm
def generate_necessary_dictionaries(graph, start_node):
    distances = {}
    unvisited = deque()
    predecessor = {}
    for key in graph:
        distances[key] = [math.inf, 0, 0]
        unvisited.append(key)
        predecessor[key] = None

    distances[start_node][0] = 0
    return distances, unvisited, predecessor


# This method generates the path from the start node to the end node
def generate_path(predecessor, end):
    path = deque()
    path.append(end)
    current = end

    while current is not None:
        path.appendleft(predecessor[current])
        current = predecessor[current]

    return list(path)


# This method finds the shortest path from a start node to a destination node
# using Dijkstra's algorithm
def shortest_path(graph: dict, start, end):
    distances, unvisited, predecessor = generate_necessary_dictionaries(graph, start)

    while unvisited:
        current_node = find_the_lowest_distance(unvisited, distances)

        if current_node == end:
            break
        for adjacent_node in graph[current_node]:
            if adjacent_node in unvisited:
                distance = distances[current_node][0] + graph[current_node][adjacent_node][0]
                if distance < distances[adjacent_node][0]:
                    distances[adjacent_node][0], distances[adjacent_node][1] = distance, graph[current_node][
                        adjacent_node][1] + distances[current_node][1]
                    predecessor[adjacent_node] = current_node

    return generate_path(predecessor, end), distances[end][0], distances[end][1]


def generate_graph():
    # Read the data from the csv file and store it in a pandas dataframe
    data = pd.read_csv("calles_de_medellin_con_acoso.csv", sep=";")

    risk_media = data["harassmentRisk"].mean()

    data["harassmentRisk"].fillna(risk_media, inplace=True)

    # Create the graph as a dictionary of dictionaries.
    # The keys of the first dictionary are the origin and
    # destination from our dataframe because they both are
    # points of the graph, where we can go or go back.
    graph = {}

    # Iterate over the origin and destination columns
    # of the dataframe and add them to the graph if they
    # are not already there.

    for i in range(len(data)):
        origin = tuple(data["origin"][i][1:-1].split(","))
        destination = tuple(data["destination"][i][1:-1].split(","))

        origin = (float(origin[1]), float(origin[0]))
        destination = (float(destination[1]), float(destination[0]))

        if origin not in graph:
            graph[origin] = {}
        # Add the adjacent street of each dictionary in the graph.
        graph[origin][destination] = (float(data["length"][i]), float(data["harassmentRisk"][i]))

        if data["oneway"][i]:
            if destination not in graph:
                graph[destination] = {}
            # Add the adjacent street of each dictionary in the graph.
            graph[destination][origin] = (float(data["length"][i]), float(data["harassmentRisk"][i]))

    del data
    return graph


def main():
    graph = generate_graph()

    path, distance, risk = shortest_path(graph, list(graph.keys())[0], list(graph.keys())[1])

    print(path, round(distance, 2), round(risk, 2))


main()

