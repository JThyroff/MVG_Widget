import mvg_api
from datetime import datetime

from src.GUI import MvgWidgetApp


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
    printFunc = switcher.get(_switch_var)
    print(_switch_var)
    printFunc(connection)


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


def test():
    now = datetime.now()
    # for debug proposes
    # now = datetime(2020, 2, 2, 19, 30, 0, 0)
    testStart = mvg_api.get_id_for_station('Forschungszentrum')
    testDest = mvg_api.get_id_for_station('Garching-Hochbrück')
    print("ID testStart: ", testStart)
    print("ID testDest: ", testDest)
    print("\n")
    routes = mvg_api.get_route(testStart, testDest, now)
    for e in routes:
        print(e)
        print_route(e)
        print("\n")
    return


if __name__ == '__main__':
    test()
    hello_kivy = MvgWidgetApp()
    hello_kivy.run()
