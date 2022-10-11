import heapq
import math
from collections import deque


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