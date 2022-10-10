import time
import pandas as pd
import math
import heapq
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
def generate_necessary_dictionaries(graph: dict, start_node):
    distances = {}
    visited = {}
    predecessor = {}
    for key in graph.keys():
        distances[key] = [math.inf, math.inf, math.inf]
        predecessor[key] = None

    distances[start_node] = [float(0), float(0), float(0)]
    return distances, visited, predecessor


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
    distances, visited, predecessor = generate_necessary_dictionaries(graph, start)
    min_distance = [(distances[start][0], distances[start][1], start)]

    while min_distance:
        distance, risk, current_node = heapq.heappop(min_distance)

        if current_node == end:
            break
        if current_node in visited:
            continue
        for adjacent_node in graph[current_node]:
            if adjacent_node not in visited:
                adj_dist = distance + graph[current_node][adjacent_node][0]
                if adj_dist < distances[adjacent_node][0]:
                    distances[adjacent_node][0], distances[adjacent_node][1] = adj_dist, graph[current_node][
                        adjacent_node][1] + risk
                    predecessor[adjacent_node] = current_node
                    heapq.heappush(min_distance, (adj_dist, distances[adjacent_node][1], adjacent_node))

    return generate_path(predecessor, end), distances[end][0], distances[end][1]


def safest_path(graph: dict, start, end):
    distances, visited, predecessor = generate_necessary_dictionaries(graph, start)
    min_distance = [(distances[start][1], distances[start][0], start)]

    while min_distance:
        risk, distance, current_node = heapq.heappop(min_distance)

        if current_node == end:
            break
        if current_node in visited:
            continue
        for adjacent_node in graph[current_node]:
            if adjacent_node not in visited:
                adj_risk = risk + graph[current_node][adjacent_node][1]
                if adj_risk < distances[adjacent_node][1]:
                    distances[adjacent_node][0], distances[adjacent_node][1] = distance + graph[current_node][
                        adjacent_node][0], adj_risk
                    predecessor[adjacent_node] = current_node
                    heapq.heappush(min_distance, (adj_risk, distances[adjacent_node][0], adjacent_node))

    return generate_path(predecessor, end), distances[end][0], distances[end][1]


def safe_short_path(graph: dict, start, end):
    distances, visited, predecessor = generate_necessary_dictionaries(graph, start)
    min_distance = [(distances[start][2], distances[start][1], distances[start][0], start)]

    while min_distance:
        melted, risk, distance, current_node = heapq.heappop(min_distance)

        if current_node == end:
            break
        if current_node in visited:
            continue
        for adjacent_node in graph[current_node]:
            if adjacent_node not in visited:
                adj_melted = melted + graph[current_node][adjacent_node][2]
                if adj_melted < distances[adjacent_node][2]:
                    distances[adjacent_node][0], distances[adjacent_node][1], distances[adjacent_node][2] = distance + \
                        graph[current_node][adjacent_node][0], risk + graph[current_node][adjacent_node][1], melted
                    predecessor[adjacent_node] = current_node
                    heapq.heappush(min_distance, (adj_melted, distances[adjacent_node][1], distances[adjacent_node][0],
                                                  adjacent_node))

    return generate_path(predecessor, end), distances[end][0], distances[end][1]


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


def main():
    graph = generate_graph()

    print("Shortest path:")
    time_start = time.time()
    path, distance, risk = shortest_path(graph, list(graph.keys())[0], list(graph.keys())[142])

    print(path, round(distance, 2), round(risk / (len(path) - 1), 2))
    print("Time: ", str(time.time() - time_start), "seconds")

    print("Safest path:")
    time_start = time.time()
    path, distance, risk = safest_path(graph, list(graph.keys())[0], list(graph.keys())[142])

    print(path, round(distance, 2), round(risk / (len(path) - 1), 2))
    print("Time: ", str(time.time() - time_start), "seconds")

    print("Safe and Short path:")
    time_start = time.time()
    path, distance, risk = safe_short_path(graph, list(graph.keys())[0], list(graph.keys())[142])

    print(path, round(distance, 2), round(risk / (len(path) - 1), 2))
    print("Time: ", str(time.time() - time_start), "seconds")


main()


