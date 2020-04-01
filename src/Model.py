import datetime
from datetime import datetime
from typing import List

import mvg_api
import requests
from kivy import Logger

from UI import MyEntry

start_str = 'Dachau'
destination_str = 'Forschungszentrum'
amount = 4

res_path = '../res/'
ok_path = 'ok/'
ok_ext = '.png'
notification_path = 'notification/'
notification_ext = '_N.png'

resources_dict = {
    "BUS": 'bus',
    "REGIONAL_BUS": 'bus',
    "SBAHN": 'sbahn',
    "UBAHN": 'ubahn',
    "TRAM": 'tram',
    "BAHN": 'regio',
    "FOOTWAY": 'walk',
    "WARNING": 'warnung'
}


def get_std_label(my_entry: MyEntry, connection):
    my_entry.destination = connection["destination"]
    my_entry.label = connection["label"]


def get_bahn_label(my_entry: MyEntry, connection):
    my_entry.destination = connection["destination"]
    my_entry.label = connection["trainType"] + ' ' + connection["label"]


def get_foot_label(my_entry: MyEntry, connection):
    my_entry.destination = my_entry.to_stat
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
    my_entry.img_ok_path = res_path + ok_path + resources_dict.get(my_entry.connection_type) + ok_ext
    my_entry.img_N_path = res_path + notification_path + resources_dict.get(my_entry.connection_type) + notification_ext
    # set label
    get_transportation_label = label_switcher.get(my_entry.connection_type)
    get_transportation_label(my_entry, connection)


def check_notifications(connection_part_list) -> bool:
    for _connection in connection_part_list:
        try:
            if _connection["notifications"] is not None:
                return True
        except:
            pass
    return False


def process_route(route) -> MyEntry:
    to_return = MyEntry()
    # should be the same as _start and _dest
    to_return.from_stat = route["from"]["name"]
    to_return.to_stat = route["to"]["name"]
    #
    _connection_part_list = route["connectionPartList"]
    # nur die erste Verbindung ist interessant
    process_connection(to_return, _connection_part_list[0])
    # trotzdem müssen alle Verbindungen auf Notifications überprüft werden
    to_return.is_notifications = check_notifications(_connection_part_list)
    to_return.departure = route["departure_datetime"].strftime("%H:%M")
    to_return.arrival = route["arrival_datetime"].strftime("%H:%M")
    return to_return


def get_route() -> str:
    return start_str + ' >> ' + destination_str


def get_next_departures() -> List[MyEntry]:
    Logger.info("Model.get_next_departures: started")
    _now = datetime.now()
    _now = datetime(2020, 3, 31, 16, 15, 0, 0)
    _list: List[MyEntry] = []
    try:
        _start = mvg_api.get_id_for_station(start_str)
        _dest = mvg_api.get_id_for_station(destination_str)
        if _start is None or _dest is None:
            raise ValueError('Route nicht definiert.', _start, _dest)
        _routes = mvg_api.get_route(_start, _dest, _now)
        for c in range(amount):
            _list.append(process_route(_routes[c]))
        Logger.info("Model.get_next_departures: normal fetch")

    except requests.exceptions.ConnectionError:
        Logger.info("Model.get_next_departures: Connectionerror")
        # error entry
        _error_entry: MyEntry = MyEntry()
        _error_entry.img_ok_path = res_path + ok_path + resources_dict.get("WARNING") + ok_ext
        _error_entry.img_N_path = res_path + notification_path + resources_dict.get("WARNING") + notification_ext
        _error_entry.label = 'Verbindungsfehler'
        _error_entry.destination = '.'
        # help entry
        _help_entry: MyEntry = MyEntry()
        _help_entry.img_ok_path = res_path + resources_dict.get("WARNING")
        _help_entry.destination = '.'
        _help_entry.label = 'WLAN überprüfen'
        # append
        _list.append(_error_entry)
        _list.append(_help_entry)
    except ValueError as verror:
        Logger.info("Model.get_next_departures: Valueerror")
        # error entry
        _error_entry: MyEntry = MyEntry()
        _error_entry.img_ok_path = res_path + ok_path + resources_dict.get("WARNING") + ok_ext
        _error_entry.img_N_path = res_path + notification_path + resources_dict.get("WARNING") + notification_ext
        _error_entry.destination = '!'
        if verror.args[1] is None:
            _error_entry.label = 'Startort unbekannt'
        elif verror.args[2] is None:
            _error_entry.label = 'Zielort unbekannt'
        # help entry
        _help_entry: MyEntry = MyEntry()
        _help_entry.img_ok_path = res_path + resources_dict.get("WARNING")
        _help_entry.destination = '!'
        _help_entry.label = 'Überprüfe die Einstellungen'
        # append
        _list.append(_error_entry)
        _list.append(_help_entry)
    finally:
        Logger.info("Model.get_next_departures: finished!")
        return _list
