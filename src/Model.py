from datetime import datetime

import mvg_api

start_str = 'Forschungszentrum'
destination_str = 'Garching-Hochbrück'


def process_connection(connection):
    pass


def process_route(route):
    _from = route["from"]["name"]
    _to = route["to"]["name"]
    _connection_part_list = route["connectionPartList"]

    process_connection(_connection_part_list[0])
    _departure = route["departure_datetime"]
    _arrival = route["arrival_datetime"]
    pass


def get_next_departures():
    _now = datetime.now()
    _start = mvg_api.get_id_for_station(start_str)
    _dest = mvg_api.get_id_for_station(destination_str)
    _routes = mvg_api.get_route(_start, _dest, _now)
    for c in range(2):
        process_route(_routes[c])
        pass
    pass
