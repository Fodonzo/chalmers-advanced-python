import networkx as nx
import matplotlib.pyplot as plt
from tramdata import read_json_data, geographical_distance  # Replace with actual imports from Lab 1
from graphs import WeightedGraph  # Replace with your implementation from Lab 2

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
            self.add_edge(stops[i].get_name(), stops[i + 1].get_name(), 1)

    def get_stop_position(self, stop_name):
        return self.stops[stop_name].get_position()

    def set_transition_time(self, stop_a, stop_b, time):
        self.add_edge(stop_a, stop_b, time)

    def list_lines_through_stop(self, stop_name):
        return self.stops[stop_name].get_lines()

    def list_stops_along_line(self, line_name):
        return [stop.get_name() for stop in self.lines[line_name].get_stops()]

    def list_all_stops(self):
        return list(self.stops.keys())

    def list_all_lines(self):
        return list(self.lines.keys())

    def extreme_positions(self):
        latitudes = [stop.get_position()[0] for stop in self.stops.values()]
        longitudes = [stop.get_position()[1] for stop in self.stops.values()]
        return min(latitudes), max(latitudes), min(longitudes), max(longitudes)


def readTramNetwork(tramfile="tramnetwork.json"):
    data = read_json_data(tramfile)  # Replace with your implementation from Lab 1
    tram_network = TramNetwork()

    for stop_name, stop_data in data["stops"].items():
        position = tuple(stop_data["position"])
        stop = TramStop(name=stop_name, position=position)
        tram_network.add_stop(stop)

    for line_name, line_data in data["lines"].items():
        line = TramLine(name=line_name)
        for stop_name in line_data["stops"]:
            line.add_stop(tram_network.stops[stop_name])
        tram_network.add_line(line)

    for (stop_a, stop_b), time in data["times"].items():
        tram_network.set_transition_time(stop_a, stop_b, time)

    return tram_network


def is_connected(graph):
    if not graph.get_vertices():
        return True

    start = next(iter(graph.get_vertices()))
    visited = set()
    queue = [start]

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            for neighbor in graph.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)

    return len(visited) == len(graph.get_vertices())


def view_shortest(graph, start, end):
    nx_graph = nx.DiGraph()
    for edge, weight in graph.get_edges():
        nx_graph.add_edge(edge[0], edge[1], weight=weight)

    try:
        shortest_path = nx.shortest_path(nx_graph, source=start, target=end, weight="weight")
        print(f"Shortest path from {start} to {end}: {shortest_path}")

        pos = nx.spring_layout(nx_graph)
        nx.draw(nx_graph, pos, with_labels=True, node_color="lightblue", edge_color="gray")
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(nx_graph, pos, edgelist=path_edges, edge_color="red", width=2)
        plt.show()

    except nx.NetworkXNoPath:
        print(f"No path found between {start} and {end}")


def demo():
    G = readTramNetwork()
    print("Checking network connectedness...")
    if is_connected(G):
        print("The tram network is connected.")
    else:
        print("The tram network is not connected.")

    a, b = input("from,to: ").split(",")
    view_shortest(G, a.strip(), b.strip())


if __name__ == "__main__":
    demo()
