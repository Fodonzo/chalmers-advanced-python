import heapq

from graphviz import Digraph

class Graph:
    def __init__(self, edgelist=None):
        self._adjacency = {}
        if edgelist:
            for start, end in edgelist:
                self.add_edge(start, end)

    def __len__(self):
        return len(self._adjacency)

    def add_vertex(self, v):
        if v not in self._adjacency:
            self._adjacency[v] = []

    def add_edge(self, a, b):
        if a not in self._adjacency:
            self.add_vertex(a)
        if b not in self._adjacency:
            self.add_vertex(b)
        self._adjacency[a].append(b)

    def edges(self):
        return [(v, u) for v in self._adjacency for u in self._adjacency[v]]

    def vertices(self):
        return list(self._adjacency.keys())

    def neighbours(self, v):
        return self._adjacency.get(v, [])

    def remove_vertex(self, v):
        if v in self._adjacency:
            del self._adjacency[v]
            for neighbours in self._adjacency.values():
                if v in neighbours:
                    neighbours.remove(v)

    def remove_edge(self, a, b):
        if a in self._adjacency and b in self._adjacency[a]:
            self._adjacency[a].remove(b)

    def set_vertex_value(self, v, x):
        if v in self._adjacency:
            self._adjacency[v] = x

    def get_vertex_value(self, v):
        return self._adjacency.get(v, [])


class WeightedGraph(Graph):
    def __init__(self, edgelist=[]):
        super().__init__(edgelist)
        self.weights = {}

        for edge in edgelist:
            if len(edge) == 3:  # Ensure weights are provided
                self.weights[(edge[0], edge[1])] = edge[2]

    def get_weight(self, a, b):
        if (a, b) not in self._edges:  # Assuming self._edges stores edges
            return None
        return self._weights.get((a, b), None)  # self._weights stores edge weights

    def set_weight(self, a, b, w):
        if (a, b) in self.edges():
            self.weights[(a, b)] = w
        else:
            raise ValueError("Edge does not exist")



def dijkstra(graph, source, cost=lambda u, v: 1):
    distances = {vertex: float('inf') for vertex in graph.vertices()}
    distances[source] = 0
    priority_queue = [(0, source)]  # (distance, vertex)
    predecessors = {vertex: None for vertex in graph.vertices()}  # To reconstruct paths

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Skip if we've already found a shorter path
        if current_distance > distances[current_vertex]:
            continue

        for neighbor in graph.neighbours(current_vertex):
            new_distance = current_distance + cost(current_vertex, neighbor)
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, predecessors  # Returns shortest distances and the path tree

def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    dot = Digraph(name, engine=engine)
    dot.attr(rankdir='LR')  # Optional: set layout direction

    # Add nodes
    for vertex in graph.vertices():
        color = nodecolors.get(vertex, 'white')
        dot.node(vertex, style='filled', fillcolor=color)class Graph:
    def __init__(self, edgelist=None):
        self._adjacency = {}
        if edgelist:
            for start, end in edgelist:
                self.add_edge(start, end)

    def __len__(self):
        return len(self._adjacency)

    def add_vertex(self, v):
        if v not in self._adjacency:
            self._adjacency[v] = []

    def add_edge(self, a, b):
        if a not in self._adjacency:
            self.add_vertex(a)
        if b not in self._adjacency:
            self.add_vertex(b)
        self._adjacency[a].append(b)

    def edges(self):
        return [(v, u) for v in self._adjacency for u in self._adjacency[v]]

    def vertices(self):
        return list(self._adjacency.keys())

    def neighbours(self, v):
        return self._adjacency.get(v, [])

    def remove_vertex(self, v):
        if v in self._adjacency:
            del self._adjacency[v]
            for neighbours in self._adjacency.values():
                if v in neighbours:
                    neighbours.remove(v)

    def remove_edge(self, a, b):
        if a in self._adjacency and b in self._adjacency[a]:
            self._adjacency[a].remove(b)

    def set_vertex_value(self, v, x):
        if v in self._adjacency:
            self._adjacency[v] = x

    def get_vertex_value(self, v):
        return self._adjacency.get(v, [])


class WeightedGraph(Graph):
    def __init__(self, edgelist=[]):
        super().__init__(edgelist)
        self.weights = {}

        for edge in edgelist:
            if len(edge) == 3:  # Ensure weights are provided
                self.weights[(edge[0], edge[1])] = edge[2]

    def get_weight(self, a, b):
        return self.weights.get((a, b), None)

    def set_weight(self, a, b, w):
        if (a, b) in self.weights:
            self.weights[(a, b)] = w
        else:
            raise ValueError("Edge does not exist")


def dijkstra(graph, source, cost=lambda u, v: 1):
    distances = {vertex: float('inf') for vertex in graph.vertices()}
    distances[source] = 0
    priority_queue = [(0, source)]  # (distance, vertex)
    predecessors = {vertex: None for vertex in graph.vertices()}  # To reconstruct paths

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Skip if we've already found a shorter path
        if current_distance > distances[current_vertex]:
            continue

        for neighbor in graph.neighbours(current_vertex):
            new_distance = current_distance + cost(current_vertex, neighbor)
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, predecessors  # Returns shortest distances and the path tree

def visualize(graph, view='dot', name='mygraph', nodecolors={}, engine='dot'):
    dot = Digraph(name, engine=engine)
    dot.attr(rankdir='LR')  # Optional: set layout direction

    # Add nodes
    for vertex in graph.vertices():
        color = nodecolors.get(vertex, 'white')
        dot.node(vertex, style='filled', fillcolor=color)

    # Add edges
    for u, v in graph.edges():
        weight = graph.get_weight(u, v) if isinstance(graph, WeightedGraph) else ""
        label = f"{weight}" if weight else ""
        dot.edge(u, v, label=label)

    # Render the graph to file
    filename = dot.render(view=view)
    print(f"Graph visualization saved as {filename}")


    # Add edges
    for u, v in graph.edges():
        weight = graph.get_weight(u, v) if isinstance(graph, WeightedGraph) else ""
        dot.edge(u, v, label=str(weight))

    # Render the graph to file
    filename = dot.render(view=view)
    print(f"Graph visualization saved as {filename}")
