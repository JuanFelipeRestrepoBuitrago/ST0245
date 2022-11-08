import time

from Entrega_3.Output import output

locations = {
    1: "EAFIT University",
    2: "National University",
    3: "University of Antioquia",
    4: "University of Medellín",
    5: "Bolivarian Pontifical University",
    6: "Colombian Polytechnic Jaime Isaza Cadavid",
    7: "Medellin's Town Hall"
}


def choose_location():
    try:
        output.menu_locations()
        option = tuple(map(int, input("Option (Example: start_option,end_option): ").split(",")))

        for i in option:
            if i < 1 or i > 7:
                raise ValueError()

        return locations[option[0]], locations[option[1]]
    except ValueError as e:
        print("Invalid Option, must be a number between 1 and 6, separated by a comma ','")
        time.sleep(1.7)
        return choose_location()
    except IndexError as e:
        print("Invalid Option, missing start or end location")
        time.sleep(1.7)
        return choose_location()
    except TypeError as e:
        print("Invalid Option, missing start or end location")
        time.sleep(1.7)
        return choose_location()


def choose_option():
    try:
        output.menu_options()
        option = input("Option: ")

        if "," in option:
            option = tuple(map(int, option.split(",")))

        else:
            option = tuple([int(option)])

        for i in option:
            if i < 1 or i > 3:
                raise ValueError()

        return option
    except ValueError:
        print("Invalid Option, must be a number between 1 and 3")
        return choose_option()


