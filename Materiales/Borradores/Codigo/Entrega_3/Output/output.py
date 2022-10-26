def shortest(start_name="Starting Point", end_name="Destination", distance=0, risk=0, path=None):
    print("Shortest Path From " + start_name + " to " + end_name)
    print("Distance:", str(round(distance, 2)), "\nHarassment Risk:", str(round(risk / (len(path) - 1), 2)))


def safest(start_name="Starting Point", end_name="Destination", distance=0, risk=0, path=None):
    print("Safest Path From " + start_name + " to " + end_name)
    print("Distance:", str(round(distance, 2)), "\nHarassment Risk:", str(round(risk / (len(path) - 1), 2)))


def safe_and_short(start_name="Starting Point", end_name="Destination", distance=0, risk=0, path=None):
    print("Safe and Short Path From " + start_name + " to " + end_name)
    print("Distance:", str(round(distance, 2)), "\nHarassment Risk:", str(round(risk / (len(path) - 1), 2)))


def menu_locations():
    print("Choose a starting point and a destination from the following list:")
    print("1. EAFIT University")
    print("2. National University")
    print("3. University of Antioquia")
    print("4. University of Medellín")
    print("5. Bolivarian Pontifical University")
    print("6. Medellin's Town Hall")


def menu_options():
    print("Choose an option from the following list:")
    print("1. Shortest Path")
    print("2. Safest Path")
    print("3. Safe and Short Path")
    print("To Choose more than one option, separate them with a comma like this: 1,2,3")
