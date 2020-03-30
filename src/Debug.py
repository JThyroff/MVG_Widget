from datetime import datetime

import mvg_api

"""
This file is for debug purposes. 
Run test() to get the next few routes between _start and _dest printed on console.
The server's JSON response will be processed accordingly.
"""


def print_bus(connection):
    _dest = connection["destination"]
    _label = connection["label"]
    print("label: ", _label)
    print("Destination: ", _dest)
    print("--------------------")
    return


def print_sbahn(connection):
    _dest = connection["destination"]
    _label = connection["label"]
    print("label: ", _label)
    print("Destination: ", _dest)
    print("--------------------")
    return


def print_ubahn(connection):
    _dest = connection["destination"]
    _label = connection["label"]
    print("label: ", _label)
    print("Destination: ", _dest)
    print("--------------------")
    return


def print_tram(connection):
    _dest = connection["destination"]
    _label = connection["label"]
    print("label: ", _label)
    print("Destination: ", _dest)
    print("--------------------")
    return


def print_bahn(connection):
    _dest = connection["destination"]
    _trainType = connection["trainType"]
    _label = connection["label"]
    print("Traintype + label: ", _trainType, _label)
    print("Destination: ", _dest)
    print("--------------------")
    return


def print_foot_way(connection):
    print("--------------------")
    return


switcher = {
    "BUS": print_bus,
    "REGIONAL_BUS": print_bus,
    "SBAHN": print_sbahn,
    "UBAHN": print_ubahn,
    "TRAM": print_tram,
    "BAHN": print_bahn,
    "FOOTWAY": print_foot_way,
}


def print_connection(connection):
    _connection_type = connection["connectionPartType"]
    _from = connection["from"]["name"]
    _to = connection["to"]["name"]

    # print("Connection Type: ", _connection_type)
    print("From: ", _from)
    print("To: ", _to)
    _switch_var = "FOOTWAY"
    if _connection_type == "TRANSPORTATION":
        _switch_var = connection["product"]
    print_func = switcher.get(_switch_var)
    print(_switch_var)
    print_func(connection)


def print_route(route):
    _from = route["from"]["name"]
    _to = route["to"]["name"]
    print("from: ", _from)
    print("to: ", _to)
    print("---------------------")
    _connection_part_list = route["connectionPartList"]

    for _connection in _connection_part_list:
        print_connection(_connection)

    _departure = route["departure_datetime"]
    print("Departure: ", _departure)
    _arrival = route["arrival_datetime"]
    print("Arrival: ", _arrival)
    return


def test(_start: str, _dest: str):
    now = datetime.now()
    # for debug proposes
    # now = datetime(2020, 3, 30, 17, 25, 0, 0)
    test_start = mvg_api.get_id_for_station(_start)
    test_dest = mvg_api.get_id_for_station(_dest)
    print("ID test_start: ", test_start)
    print("ID test_dest: ", test_dest)
    print("\n")
    routes = mvg_api.get_route(test_start, test_dest, now)
    for e in routes:
        print(e)
        print_route(e)
        print("\n")
    return


if __name__ == '__main__':
    test('Dachau', 'Hauptbahnhof')
