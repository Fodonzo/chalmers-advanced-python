from graphs import WeightedGraph
import json
from graphviz import Digraph

class TramStop:
    def __init__(self, name, position=None, lines=None):
        self.name = name
        self.position = position if position else (0, 0)
        self.lines = lines if lines else []

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

    def set_position(self, position):
        self.position = position

    def get_lines(self):
        return self.lines

    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)


class TramLine:
    def __init__(self, name, stops=None):
        self.name = name
        self.stops = stops if stops else []

    def get_name(self):
        return self.name

    def get_stops(self):
        return self.stops

    def add_stop(self, stop):
        if stop not in self.stops:
            self.stops.append(stop)


class TramNetwork(WeightedGraph):
    def __init__(self):
        super().__init__()
        self.stops = {}
        self.lines = {}

    def add_stop(self, stop):
        self.stops[stop.get_name()] = stop
        self.add_vertex(stop.get_name())

    def add_line(self, line):
        self.lines[line.get_name()] = line
        stops = line.get_stops()
        for i in range(len(stops) - 1):
            self.add_edge(stops[i].get_name(), stops[i + 1].get_name())
            self.set_weight(stops[i].get_name(), stops[i + 1].get_name(), 1)

    def set_transition_time(self, stop_a, stop_b, time):
        self.add_edge(stop_a, stop_b)
        self.set_weight(stop_a, stop_b, time)

    def list_all_stops(self):
        return list(self.stops.keys())

    def list_all_lines(self):
        return list(self.lines.keys())

    def lines_via_stop(self, stop_name):
        stop = self.stops.get(stop_name)
        if not stop:
            raise KeyError(f"Stop {stop_name} does not exist in the network.")
        return stop.get_lines()

    def lines_between_stops(self, stop_a, stop_b):
        if stop_a not in self.stops or stop_b not in self.stops:
            raise KeyError(f"One or both stops {stop_a}, {stop_b} do not exist in the network.")
        lines_a = set(self.stops[stop_a].get_lines())
        lines_b = set(self.stops[stop_b].get_lines())
        return list(lines_a & lines_b)

    def time_between_stops(self, stop_a, stop_b):
        if not self.has_edge(stop_a, stop_b):
            raise ValueError(f"No direct connection exists between {stop_a} and {stop_b}.")
        return self.get_weight(stop_a, stop_b)


def build_tram_network(json_file="tramnetwork.json"):
    """
    Constructs a TramNetwork object from a JSON file.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    tram_network = TramNetwork()

    # Add stops to the network
    for stop_name, stop_data in data["stops"].items():
        position = (stop_data["lat"], stop_data["lon"])
        stop = TramStop(name=stop_name, position=position)
        tram_network.add_stop(stop)

    # Add lines and their respective stops
    for line_name, stops in data["lines"].items():
        line = TramLine(name=f"Line {line_name}")
        for stop_name in stops:
            stop = tram_network.stops[stop_name]
            line.add_stop(stop)
            stop.add_line(f"Line {line_name}")
        tram_network.add_line(line)

    # Add transition times between stops
    for stop_a, connections in data["times"].items():
        for stop_b, time in connections.items():
            tram_network.set_transition_time(stop_a, stop_b, time)

    return tram_network


def export_to_graphviz(network, filename="tram_network"):
    """
    Exports the tram network to a Graphviz DOT file for visualization.
    """
    dot = Digraph(name=filename, format="png")

    # Add nodes (stops)
    for stop_name in network.list_all_stops():
        dot.node(stop_name)

    # Add edges (connections between stops)
    for stop_a, stop_b in network.edges():
        weight = network.get_weight(stop_a, stop_b)
        dot.edge(stop_a, stop_b, label=str(weight))

    # Save and render the graph
    dot.render(filename, view=True)
    print(f"Graph exported to {filename}.dot and rendered.")


# Example Usage
if __name__ == "__main__":
    network = build_tram_network()
    print("Tram network loaded with stops:", network.list_all_stops())
    print("And lines:", network.list_all_lines())

    # Export the network to Graphviz
    export_to_graphviz(network, filename="tram_network")
