from graphs import WeightedGraph
from haversine import haversine, Unit
import json

class TramNetwork(WeightedGraph):
    def __init__(self, lines=None, stops=None, times=None):
        super().__init__()
        self._linedict = {}
        self._stopdict = {}
        self._timedict = {}

        if lines:
            for line in lines:
                self.add_line(line)
        if stops:
            for stop in stops:
                self.add_stop(stop)
        if times:
            for (a, b), time in times.items():
                self.set_transition_time(a, b, time)

    def all_lines(self):
        return list(self._linedict.keys())

    def all_stops(self):
        return list(self._stopdict.keys())

    def add_line(self, line):
        self._linedict[line.get_number()] = line

    def add_stop(self, stop):
        self._stopdict[stop.get_name()] = stop

    def stop_lines(self, stop_name):
        if stop_name not in self._stopdict:
            raise ValueError(f"Stop '{stop_name}' not found.")
        return self._stopdict[stop_name].get_lines()

    def stop_position(self, stop_name):
        if stop_name not in self._stopdict:
            raise ValueError(f"Stop '{stop_name}' not found.")
        return self._stopdict[stop_name].get_position()

    def line_stops(self, line_number):
        if line_number not in self._linedict:
            raise ValueError(f"Line '{line_number}' not found.")
        return self._linedict[line_number].get_stops()

    def geo_distance(self, a, b):
        if a not in self._stopdict or b not in self._stopdict:
            raise ValueError(f"One or both stops not found: {a}, {b}")
        lat1, lon1 = self.stop_position(a)
        lat2, lon2 = self.stop_position(b)
        return haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)

    def transition_time(self, a, b):
        return self._timedict.get((a, b), None)

    def set_transition_time(self, a, b, time):
        self._timedict[(a, b)] = time

    def extreme_positions(self):
        positions = [stop.get_position() for stop in self._stopdict.values()]
        latitudes = [pos[0] for pos in positions]
        longitudes = [pos[1] for pos in positions]
        return (min(latitudes), max(latitudes)), (min(longitudes), max(longitudes))

    @staticmethod
    def readTramNetwork(file='tramnetwork.json'):
        with open(file, 'r') as f:
            data = json.load(f)

        # Create TramStops
        stops = {}
        for stop_data in data['stops']:
            name = stop_data['name']
            lines = stop_data['lines']
            lat, lon = stop_data['position']
            stops[name] = TramStop(name, lines, lat, lon)

        # Create TramLines
        lines = {}
        for line_data in data['lines']:
            number = line_data['number']
            stop_names = line_data['stops']
            line_stops = [stops[stop_name] for stop_name in stop_names]
            lines[number] = TramLine(number, line_stops)

        # Create transition times
        times = {}
        for transition, time in data['times'].items():
            a, b = transition.split("->")
            times[(a, b)] = time

        # Create and return the TramNetwork
        return TramNetwork(lines.values(), stops.values(), times)


class TramStop:
    def __init__(self, name, lines, lat, lon):
        self._name = name
        self._lines = lines  # List of tram lines stopping here
        self._position = (lat, lon)

    def get_name(self):
        return self._name

    def get_lines(self):
        return self._lines

    def get_position(self):
        return self._position

    def set_position(self, lat, lon):
        self._position = (lat, lon)

    def add_line(self, line):
        if line not in self._lines:
            self._lines.append(line)


class TramLine:
    def __init__(self, number, stops):
        self._number = number
        self._stops = stops  # List of TramStop objects

    def get_number(self):
        return self._number

    def get_stops(self):
        return self._stops


# Testing
if __name__ == "__main__":
    stop1 = TramStop("Stop A", ["Line 1"], 59.3293, 18.0686)
    stop2 = TramStop("Stop B", ["Line 1"], 59.3324, 18.0649)
    stop3 = TramStop("Stop C", ["Line 2"], 59.3350, 18.0618)

    line1 = TramLine("Line 1", [stop1, stop2])
    line2 = TramLine("Line 2", [stop2, stop3])

    times = {("Stop A", "Stop B"): 5, ("Stop B", "Stop C"): 7}

    tram_network = TramNetwork([line1, line2], [stop1, stop2, stop3], times)

    print("All stops:", tram_network.all_stops())
    print("All lines:", tram_network.all_lines())
    print("Distance between Stop A and Stop B:", tram_network.geo_distance("Stop A", "Stop B"))
    print("Transition time from Stop A to Stop B:", tram_network.transition_time("Stop A", "Stop B"))

    # Reading network from file (uncomment to test)
    # tram_network_from_file = TramNetwork.readTramNetwork("tramnetwork.json")
    # print("Stops from file:", tram_network_from_file.all_stops())
