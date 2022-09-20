import pandas as pd
import math
import queue


def find_lower_distance(unvisited: queue, distances: dict):
    pass


def dijkstra_distance(graph: dict, start: str, end: str):
    pass


def main():
    # Read the data from the csv file and store it in a pandas dataframe
    data = pd.read_csv("calles_de_medellin_con_acoso.csv", sep=";")

    # Create the graph as a dictionary of dictionaries.
    # The keys of the first dictionary are the origin and
    # destination from our dataframe because they both are
    # points of the graph, where we can go or go back.
    graph = {}

    # Iterate over the origin and destination columns
    # of the dataframe and add them to the graph if they
    # are not already there.
    for i in range(len(data)):
        if data["origin"][i] not in graph:
            graph[data["origin"][i]] = {}
        if data["destination"][i] not in graph:
            graph[data["destination"][i]] = {}

        # Add the adjacent street of each dictionary in the graph.
        graph[data["origin"][i]][data["destination"][i]] = (data["length"][i], data["harassmentRisk"][i])
        graph[data["destination"][i]][data["origin"][i]] = (data["length"][i], data["harassmentRisk"][i])


main()

