import json
import sys

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

def lines_via_stop(linedict, stop):
    stops_at_stop = []

    for line_number, stops in linedict.items():
        if stop in stops:
            stops_at_stop.append(line_number)

    stops_at_stop.sort()

    return stops_at_stop


def lines_between_stops(linedict, stop1, stop2):

    lines_that_pass_both_stops = []

    for line_number, stops in linedict.items():
        if stop1 in stops and stop2 in stops:
            index1 = stops.index(stop1)
            index2 = stops.index(stop2)

            if abs(index1 - index2) == 1:
                lines_that_pass_both_stops.append(int(line_number))

    lines_that_pass_both_stops.sort()
    return [str(line) for line in lines_that_pass_both_stops]


def time_between_stops(linedict, timedict, line, stop1, stop2):

    if line not in linedict:
        return f"Line {line} not found in linedict"

    stops = linedict[line]

    if stop1 not in stops or stop2 not in stops:
        return f"Stops {stop1} and/or {stop2} are not on line {line}"

    if stop1 == stop2:
        return 0

    index1 = stops.index(stop1)
    index2 = stops.index(stop2)

    if index1 < index2:
        path = stops[index1:index2]
    else:
        path = stops[index1:index2-1]


    total_time = 0

    for i in range(len(path)-1):
        current_stop = path[i]
        next_stop = path[i+1]

        if next_stop in timedict[current_stop]:
            total_time += timedict[current_stop][next_stop]
        else:
            return f"Stop {current_stop} not on line {line}"

    return total_time

from haversine import haversine

def distance_between_stops(stopdict, stop1, stop2):
    if stop1 not in stopdict or stop2 not in stopdict:
        return f"{stop1} and/or {stop2} are not found in stopdict"

    coord1 = stopdict[stop1]
    coord2 = stopdict[stop2]

    if not (isinstance(coord1, (list, tuple)) and isinstance(coord2, (list, tuple))):
        return f"Coordinates for {stop1} or {stop2} are not valid"

    if stop1 == stop2:
        return 0

    return haversine(coord1, coord2)


def answer_query(tramdict, query):
    linedict = tramdict['linedict']
    timedict = tramdict['timedict']
    stopdict = tramdict['stopdict']

    query = query.strip().lower()

    try:
        if query.startswith("lines via"):
            stop = query.split("via", 1)[1].strip()
            return lines_via_stop(linedict, stop)

        elif query.startswith("lines between"):
            _, stops = query.split("between", 1)
            stop1, stop2 = map(str.strip, stops.split("and"))
            return lines_between_stops(linedict, stop1, stop2)

        elif query.startswith("time between"):
            parts = query.split("on line")
            stops_part = parts[0].split("between", 1)[1].strip()
            stop1, stop2 = map(str.strip, stops_part.split("and"))
            line = parts[1].strip()
            return time_between_stops(linedict, timedict, line, stop1, stop2)

        elif query.startswith("distance between"):
            _, stops = query.split("between", 1)
            stop1, stop2 = map(str.strip, stops.split("and"))
            return distance_between_stops(stopdict, stop1, stop2)

        else:
            return False

    except Exception:
        return False




def dialogue(tramfile):
    tramdict = {
        "linedict": {},
        "timedict": {},
        "stopdict": {}
    }

    with open(tramfile, 'r', encoding='utf-8') as file:
        tramdict = json.load(file)

    print("Welcome to the Tram System. Type your query or 'quit' to exit.")

    while True:
        query = input("Enter your query: ").strip()

        if query.lower() == 'quit':
            print("Goodbye!")
            break

        result = answer_query(tramdict, query)
        if result is False:
            print("I couldn't understand your query. Please try again.")
        else:
            print("Result:", result)


    if __name__ == '__main__':
        if sys.argv[1:] == ['init']:
            build_tram_network("tramlines.txt", "tramstops.json")
        else:
            dialogue("tramnetwork.json")
