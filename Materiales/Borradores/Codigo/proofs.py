import time
from collections import deque

import pandas as pd
import math
import heapq


# This method finds the vertex of the graph with the lowest distance
# of all vertexes that are in unvisited
def find_the_lowest_distance(unvisited: deque, distances: dict):
    lowest_key = min(unvisited, key=lambda vertex: distances[vertex])
    unvisited.remove(lowest_key)
    return lowest_key


# def find_the_lowest_distance1(unvisited: deque, distances: dict):
#     lowest_key = ""
#     lowest = math.inf
#
#     for node in unvisited:
#         if distances[node][0] < lowest:
#             lowest_key = node
#             lowest = distances[node][0]
#
#     unvisited.remove(lowest_key)
#     return lowest_key


# This method generates the necessary dictionaries to run dijkstra's algorithm
def generate_necessary_dictionaries(graph: dict, start_node):
    distances = dict.fromkeys(graph.keys(), math.inf)
    risks = dict.fromkeys(graph.keys(), math.inf)
    unvisited = {}
    predecessor = dict.fromkeys(graph.keys(), None)

    distances[start_node] = float(0)
    risks[start_node] = float(0)
    return distances, risks, unvisited, predecessor


# This method generates the path from the start node to the end node
def generate_path(predecessor, end):
    path = deque()
    path.append(end)
    current = end

    while predecessor[current] is not None:
        path.appendleft(predecessor[current])
        current = predecessor[current]

    return list(path)


# This method finds the shortest path from a start node to a destination node
# using Dijkstra's algorithm
def shortest_path(graph: dict, start, end):
    distances, risks, visited, predecessor = generate_necessary_dictionaries(graph, start)
    min_distance = [(float(0), float(0), start)]

    while min_distance:
        distance, risk, current_node = heapq.heappop(min_distance)

        if current_node == end:
            break
        if current_node in visited:
            continue
        for adjacent_node in graph[current_node]:
            if adjacent_node not in visited:
                adj_dist = distance + graph[current_node][adjacent_node][0]
                if adj_dist < distances[adjacent_node]:
                    distances[adjacent_node], risks[adjacent_node] = adj_dist, graph[current_node][
                        adjacent_node][1] + risk
                    predecessor[adjacent_node] = current_node
                    heapq.heappush(min_distance, (adj_dist, risks[adjacent_node], adjacent_node))

    return generate_path(predecessor, end), distances[end], risks[end]


def safest_path(graph: dict, start, end):
    distances, risks, visited, predecessor = generate_necessary_dictionaries(graph, start)
    min_distance = [(distances[start], distances[start], start)]

    while min_distance:
        risk, distance, current_node = heapq.heappop(min_distance)

        if current_node == end:
            break
        if current_node in visited:
            continue
        for adjacent_node in graph[current_node]:
            if adjacent_node not in visited:
                adj_risk = risk + graph[current_node][adjacent_node][1]
                if adj_risk < risks[adjacent_node]:
                    distances[adjacent_node], risks[adjacent_node] = distance + graph[current_node][
                        adjacent_node][0], adj_risk
                    predecessor[adjacent_node] = current_node
                    heapq.heappush(min_distance, (adj_risk, distances[adjacent_node], adjacent_node))

    return generate_path(predecessor, end), distances[end], risks[end]


def safe_short_path(graph: dict, start, end):
    pass


def generate_graph():
    # Read the data from the csv file and store it in a pandas dataframe
    data = pd.read_csv("Entrega_2\calles_de_medellin_con_acoso.csv", sep=";")

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


def main():
    graph = generate_graph()

    # print("Functional")
    # time_start = time.time()
    # distances, unvisited, predecessor = generate_necessary_dictionaries(graph, list(graph.keys())[2000])
    # find_the_lowest_distance(unvisited, distances)
    # print("Time: ", str((time.time() - time_start)), "seconds")
    #
    # print("Non-Functional")
    # time_start = time.time()
    # distances, unvisited, predecessor = generate_necessary_dictionaries(graph, list(graph.keys())[2000])
    # find_the_lowest_distance1(unvisited, distances)
    # print("Time: ", str((time.time() - time_start)), "seconds")

    print("Shortest path:")
    time_start = time.time()
    path, distance, risk = shortest_path(graph, list(graph.keys())[0], list(graph.keys())[2000])

    print(path, round(distance, 2), round(risk / (len(path) - 1), 2))
    print("Time: ", str(time.time() - time_start), "seconds")

    print("Safest path:")
    time_start = time.time()
    path, distance, risk = safest_path(graph, list(graph.keys())[0], list(graph.keys())[2000])

    print(path, round(distance, 2), round(risk / (len(path) - 1), 2))
    print("Time: ", str(time.time() - time_start), "seconds")


main()
