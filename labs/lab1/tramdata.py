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
    lines = [line for line, stops in linedict.items() if stop in map(str.lower, stops)]
    return sorted(lines, key=lambda x: int(x))

def lines_between_stops(linedict, stop1, stop2):
    stop1 = stop1.lower()
    stop2 = stop2.lower()

    lines_that_pass_both_stops = []

    for line_number, stops in linedict.items():
        stops_lower = [s.lower() for s in stops]

        if stop1 in stops_lower and stop2 in stops_lower:
            index1 = stops_lower.index(stop1)
            index2 = stops_lower.index(stop2)

            if index1 is not None and index2 is not None:
                lines_that_pass_both_stops.append(line_number)

    lines_that_pass_both_stops.sort()

    return lines_that_pass_both_stops


def time_between_stops(linedict, timedict, line, stop1, stop2):
    if line not in linedict:
        return f"Line {line} not found in linedict"

    stops = linedict[line]

    stop1 = stop1.lower()
    stop2 = stop2.lower()

    if stop1 not in [s.lower() for s in stops]:
        return f"Stop {stop1} not found on line {line}"
    if stop2 not in [s.lower() for s in stops]:
        return f"Stop {stop2} not found on line {line}"

    if stop1 == stop2:
        return 0

    try:
        index1 = next(i for i, s in enumerate(stops) if s.lower() == stop1)
        index2 = next(i for i, s in enumerate(stops) if s.lower() == stop2)
        print(f"Indices - Stop1: {index1}, Stop2: {index2}")  # Debugging line
    except ValueError as e:
        return f"Error finding stops: {e}"

    if index1 < index2:
        path = stops[index1:index2 + 1]
    else:
        path = stops[index2:index1 + 1][::-1]

    total_time = 0
    for i in range(len(path) - 1):
        current_stop = path[i]
        next_stop = path[i + 1]

        if next_stop in timedict[current_stop]:
            transition_time = timedict[current_stop][next_stop]
            total_time += transition_time
        else:
            return f"No time data between {current_stop} and {next_stop}"

    return total_time

from haversine import haversine, Unit

def distance_between_stops(stopdict, stop1, stop2):
    stop1 = stop1.strip().lower()
    stop2 = stop2.strip().lower()

    stops_normalized = {key.strip().lower(): key for key in stopdict.keys()}

    if stop1 not in stops_normalized or stop2 not in stops_normalized:
        return f"{stop1.capitalize()} and/or {stop2.capitalize()} are not found in stopdict"

    original_stop1 = stops_normalized[stop1]
    original_stop2 = stops_normalized[stop2]

    coord1 = stopdict[original_stop1]
    coord2 = stopdict[original_stop2]

    if not all(
        isinstance(coord, dict) and "lat" in coord and "lon" in coord
        for coord in [coord1, coord2]
    ):
        return f"Invalid coordinates for {original_stop1} or {original_stop2}. Expected format: {{'lat': <value>, 'lon': <value>}}"

    if stop1 == stop2:
        return 0

    distance = haversine(
        (coord1["lat"], coord1["lon"]),
        (coord2["lat"], coord2["lon"]),
        unit=Unit.KILOMETERS
    )

    return distance


def answer_query(tramdict, query):
    linedict = tramdict['lines']
    timedict = tramdict['times']
    stopdict = tramdict['stops']

    query = query.strip().lower()

    try:
        if query.startswith("lines via"):
            stop = query.split("via", 1)[1].strip().lower()
            return lines_via_stop(linedict, stop)

        elif query.startswith("lines between"):
            _, stops = query.split("between", 1)
            stop1, stop2 = map(str.strip, stops.split("and"))
            stop1 = stop1.lower()
            stop2 = stop2.lower()
            return lines_between_stops(linedict, stop1, stop2)

        elif query.startswith("time between"):
            parts = query.split("between", 1)
            stops_part = parts[1].split("on line")

            stop1, stop2 = map(str.strip, stops_part[0].split("and"))
            line = stops_part[1].strip()

            stop1 = stop1.lower()
            stop2 = stop2.lower()

            return time_between_stops(linedict, timedict, line, stop1, stop2)

        elif query.startswith("distance between"):
            _, stops = query.split("between", 1)
            stop1, stop2 = map(str.strip, stops.split("and"))
            return distance_between_stops(stopdict, stop1, stop2)

        else:
            print("Query not recognized.")  # Debugging line
            return False

    except Exception as e:
        print(f"Error processing query: {e}")  # Debugging line
        return f"Error: {str(e)}"

def dialogue(tramfile):
    try:
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

    except FileNotFoundError:
        print(f"Error: Could not find file {tramfile}. Please ensure the tram network is initialized.")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'init':
        print("Initializing tram network...")
        build_tram_network(
            "C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/lab1/tramstops.json",
            "C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/lab1/tramlines.txt"
        )

        print("Tram network initialized. Exiting.")
    else:
        dialogue("C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/lab1/tramnetwork.json")
