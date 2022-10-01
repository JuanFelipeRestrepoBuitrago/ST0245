import pandas as pd
import math
import queue


# This method finds the vertex of the graph with the lowest distance
# of all vertexes that are in unvisited
def find_the_lowest_distance(unvisited: queue, distances: dict):
    lowest_key = ""
    lowest = math.inf

    for node in unvisited:
        if distances[node] < lowest:
            lowest_key = node
            lowest = distances[node]

    return lowest_key


def dijkstra_distance(graph: dict, start: str, end: str):
    pass


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
    print(graph)
    print(len(graph))


main()

