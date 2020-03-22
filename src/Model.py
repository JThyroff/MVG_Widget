from datetime import datetime
from typing import List

import mvg_api

from GUI import MyEntry

start_str = 'Forschungszentrum'
destination_str = 'Garching-Hochbrück'

res_path = '../res/'

resources_dict = {
    "BUS": 'bus.png',
    "REGIONAL_BUS": 'bus.png',
    "SBAHN": 'sbahn.png',
    "UBAHN": 'ubahn.png',
    "TRAM": 'tram.png',
    "BAHN": 'bahn.png',
    "FOOTWAY": 'walk.png',
}


def get_std_label(my_entry: MyEntry, connection):
    my_entry.destination = connection["destination"]
    my_entry.label = connection["label"]


def get_bahn_label(my_entry: MyEntry, connection):
    my_entry.destination = connection["destination"]
    my_entry.label = connection["trainType"] + ' ' + connection["label"]


def get_foot_label(my_entry: MyEntry, connection):
    my_entry.destination = my_entry.to_
    my_entry.label = 'Zu Fuß'


label_switcher = {
    "BUS": get_std_label,
    "REGIONAL_BUS": get_std_label,
    "SBAHN": get_std_label,
    "UBAHN": get_std_label,
    "TRAM": get_std_label,
    "BAHN": get_bahn_label,
    "FOOTWAY": get_foot_label,
}


def process_connection(my_entry: MyEntry, connection):
    _c_part_type = connection["connectionPartType"]
    my_entry.connection_type = "FOOTWAY"
    if _c_part_type == "TRANSPORTATION":
        my_entry.connection_type = connection["product"]
    # set image path
    my_entry.img_path = res_path + resources_dict.get(my_entry.connection_type)
    # set label
    get_transportation_label = label_switcher.get(my_entry.connection_type)
    get_transportation_label(my_entry, connection)


def process_route(route) -> MyEntry:
    to_return = MyEntry()
    # should be the same as _start and _dest
    to_return.from_ = route["from"]["name"]
    to_return.to_ = route["to"]["name"]
    #
    _connection_part_list = route["connectionPartList"]
    # nur die erste Verbindung ist interessant
    process_connection(to_return, _connection_part_list[0])
    to_return.departure = route["departure_datetime"]
    to_return.arrival = route["arrival_datetime"]
    return to_return


def get_next_departures() -> List[MyEntry]:
    _now = datetime.now()
    _start = mvg_api.get_id_for_station(start_str)
    _dest = mvg_api.get_id_for_station(destination_str)
    _routes = mvg_api.get_route(_start, _dest, _now)
    _list: List[MyEntry] = []
    for c in range(2):
        _list.append(process_route(_routes[c]))
    return _list
