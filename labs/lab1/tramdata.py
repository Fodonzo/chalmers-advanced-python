import json

def build_tram_stops(jsonobject):
    with open(jsonobject, 'r', encoding='utf-8') as file:
        data = json.load(file)

    stops_dict = {}

    for stop_name, stop_info in data.items():
        latitude = float(stop_info['position'][0])
        longitude = float(stop_info['position'][1])

        stops_dict[stop_name] = {
            'lat': latitude,
            'lon': longitude
        }

    return stops_dict


def build_tram_lines(linefile):
    line_dict = {}
    time_dict = {}

    with open(linefile, 'r', encoding='utf-8') as file:
        current_line = None
        previous_stop = None
        previous_time = 0

        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.endswith(':'):
                current_line = line[:-1].strip()
                line_dict[current_line] = []
                previous_stop = None
                previous_time = 0

            elif current_line is not None:
                try:
                    stop, time = line.rsplit(maxsplit=1)
                    hour, minute = map(int, time.split(':'))
                    time_in_minutes = hour * 60 + minute

                    line_dict[current_line].append(stop)

                    if previous_stop is not None:
                        transition_time = time_in_minutes - previous_time

                        if previous_stop not in time_dict:
                            time_dict[previous_stop] = {}
                        if stop not in time_dict:
                            time_dict[stop] = {}

                        time_dict[previous_stop][stop] = transition_time
                        time_dict[stop][previous_stop] = transition_time

                    previous_stop = stop
                    previous_time = time_in_minutes

                except ValueError:
                    continue

    return line_dict, time_dict


def build_tram_network(stopfile, linefile):

    stops_dict = build_tram_stops(stopfile)
    lines_dict, times_dict = build_tram_lines(linefile)

    tram_network = {
        "stops": stops_dict,
        "lines": lines_dict,
        "times": times_dict
    }

    with open('tramnetwork.json', 'w', encoding='utf-8') as outfile:
        json.dump(tram_network, outfile, ensure_ascii=False, indent=4)


build_tram_network(
    'C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/data/tramstops.json',
    'C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/data/tramlines.txt'
)
