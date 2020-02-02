import mvg_api
import json
from datetime import datetime


def print_bus():
    return


def print_bahn():
    pass


def print_sbahn():
    pass


def print_ubahn():
    pass


def print_foot_way(connection):
    _from = connection["from"]["name"]
    _to = connection["to"]["name"]
    print("Footway")
    print("From: ", _from)
    print("To: ", _to)
    return


switcher = {
    "BUS": print_bus,
    "BAHN": print_bahn,
    "SBAHN": print_sbahn,
    "UBAHN": print_ubahn,
    "FOOTWAY": print_foot_way,
}


def print_connection(connection):
    connectionType = connection["connectionPartType"]
    printFunc = switcher.get(connectionType)
    printFunc()


def print_connection_list(connectionlist):
    _from = connectionlist["from"]["name"]
    _to = connectionlist["to"]["name"]
    print("from: ", _from)
    print("to: ", _to)
    _prod = connectionlist["connectionPartList"][0]["product"]
    print("product: ", _prod)
    if _prod == "SBAHN":
        # SBAHN MODE
        _dest = connectionlist["connectionPartList"][0]["destination"]
        _label = connectionlist["connectionPartList"][0]["label"]
        print("label: ", _label)
        print("Destination: ", _dest)
    elif _prod == "BAHN":
        # REGIO MODE
        _dest = connectionlist["connectionPartList"][0]["destination"]
        _trainType = connectionlist["connectionPartList"][0]["trainType"]
        _label = connectionlist["connectionPartList"][0]["label"]
        print("Traintype + label: ", _trainType, _label)
        print("Destination: ", _dest)
        # Fußweg ignorieren

    _departure = connectionlist["departure_datetime"]
    print("Departure: ", _departure)
    _arrival = connectionlist["arrival_datetime"]
    print("Arrival: ", _arrival)
    return


def test():
    now = datetime.now()
    # for debug proposes
    now = datetime(2020, 2, 2, 19, 30, 0, 0)
    testStation = mvg_api.get_id_for_station('Königsplatz')
    münchen = mvg_api.get_id_for_station('München Hauptbahnhof')
    # idd = 'de:09174:6800'
    routes = mvg_api.get_route(testStation, münchen, now)
    for e in routes:
        print(e)
        print_connection_list(e)
        print("\n")
    return


if __name__ == '__main__':
    test()
