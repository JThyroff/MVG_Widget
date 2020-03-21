from datetime import datetime

import mvg_api

from GUI import MyEntry

start_str = 'Forschungszentrum'
destination_str = 'Garching-Hochbrück'


def get_std(connection)->:
    pass

switcher = {
    "BUS": print_bus,
    "REGIONAL_BUS": print_bus,
    "SBAHN": print_sbahn,
    "UBAHN": print_ubahn,
    "TRAM": print_tram,
    "BAHN": print_bahn,
    "FOOTWAY": print_foot_way,
}

def process_connection(connection):
    _connection_type = connection["connectionPartType"]
    _switch_var = "FOOTWAY"
    if _connection_type == "TRANSPORTATION":
        _switch_var = connection["product"]
    get_transportation_label = switcher.get(_switch_var)
    lbl = get_transportation_label(connection)
    pass


def process_route(route) -> MyEntry:
    to_return = MyEntry()
    # should be the same as _start and _dest
    _from = route["from"]["name"]
    _to = route["to"]["name"]
    #
    _connection_part_list = route["connectionPartList"]
    # nur die erste Verbindung ist interessant
    process_connection(_connection_part_list[0])
    _departure = route["departure_datetime"]
    _arrival = route["arrival_datetime"]
    return to_return


def get_next_departures():
    _now = datetime.now()
    _start = mvg_api.get_id_for_station(start_str)
    _dest = mvg_api.get_id_for_station(destination_str)
    _routes = mvg_api.get_route(_start, _dest, _now)
    for c in range(2):
        process_route(_routes[c])
        pass