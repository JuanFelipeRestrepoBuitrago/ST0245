from Entrega_3.Output import output

locations = {
    1: "Universidad EAFIT",
    2: "Universidad Nacional",
    3: "Universidad de Antioquia",
    4: "Universidad de Medellín",
    5: "Universidad Pontificia Bolivariana",
    6: "Alcaldia de Medellín"
}


def choose_location():
    output.menu_locations()
    option = tuple(map(int, input("Option (Example: start_option,end_option): ").split(",")))

    return (locations[option[0]], locations[option[1]])


def choose_option():
    output.menu_options()
    option = input("Option: ")

    if "," in option:
        option = tuple(map(int, option.split(",")))
    else:
        option = (int(option))

    return option


