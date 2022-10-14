import dijkstra as d
import pandas as pd
import draw


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
