import mvg_api
import json
from datetime import datetime


def printConnection(connection):
    _from = connection["from"]["name"]
    _to = connection["to"]["name"]
    print("from: ", _from)
    print("to: ", _to)
    _prod = connection["connectionPartList"][0]["product"]
    print("product: ", _prod)
    if _prod == "SBAHN":
        # SBAHN MODE
        _dest = connection["connectionPartList"][0]["destination"]
        _label = connection["connectionPartList"][0]["label"]
        print("label: ", _label)
        print("Destination: ", _dest)
    elif _prod == "BAHN":
        # REGIO MODE
        _dest = connection["connectionPartList"][0]["destination"]
        _trainType = connection["connectionPartList"][0]["trainType"]
        _label = connection["connectionPartList"][0]["label"]
        print("Traintype + label: ", _trainType, _label)
        print("Destination: ", _dest)
        # Fußweg ignorieren

    _departure = connection["departure_datetime"]
    print("Departure: ", _departure)
    _arrival = connection["arrival_datetime"]
    print("Arrival: ", _arrival)


def test():
    now = datetime.now()
    # for debug proposes
    # now = datetime(2020, 2, 2, 19, 30, 0, 0)
    dachau = mvg_api.get_id_for_station('Dachau')
    münchen = mvg_api.get_id_for_station('München Hauptbahnhof')
    # idd = 'de:09174:6800'
    routes = mvg_api.get_route(dachau, münchen, now)
    for e in routes:
        printConnection(e)
        print("\n")


if __name__ == '__main__':
    test()
