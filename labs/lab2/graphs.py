import heapq

from graphviz import Digraph

import networkx as nx

class Graph(nx.Graph):
    def __init__(self, edgelist=None):
        """
        Initialize the graph. If edgelist is provided, add the edges to the graph.
        """
        super().__init__()
        if edgelist:
            self.add_edges_from(edgelist)

    def vertices(self):
        """
        Return a list of all vertices in the graph.
        """
        return list(self.nodes)

    def edges(self):
        """
        Return a list of edges in the graph.
        """
        return list(super().edges)

    def neighbors(self, vertex):
        """
        Return a list of neighbors for a given vertex.
        """
        return list(self.neighbors(vertex))

    def add_vertex(self, vertex):
        """
        Add a vertex to the graph.
        """
        self.add_node(vertex)

    def add_edge(self, vertex1, vertex2):
        """
        Add an edge between two vertices.
        """
        super().add_edge(vertex1, vertex2)

    def remove_vertex(self, vertex):
        """
        Remove a vertex and its associated edges from the graph.
        """
        self.remove_node(vertex)

    def remove_edge(self, vertex1, vertex2):
        """
        Remove an edge between two vertices.
        """
        self.remove_edge(vertex1, vertex2)

    def get_vertex_value(self, vertex):
        """
        Get the value associated with a vertex. Returns None if no value is set.
        """
        return self.nodes[vertex].get("value", None)

    def set_vertex_value(self, vertex, value):
        """
        Set a value for a vertex.
        """
        self.nodes[vertex]["value"] = value

    def __len__(self):
        """
        Return the number of vertices in the graph.
        """
        return self.number_of_nodes()



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
        dot.node(vertex, style='filled', fillcolor=color)
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

    def get_weight(self, vertex1, vertex2):
        """
        Get the weight of the edge between vertex1 and vertex2.
        """
        return self[vertex1][vertex2].get("weight", None)

    def set_weight(self, vertex1, vertex2, weight):
        """
        Set the weight of the edge between vertex1 and vertex2.
        """
        self[vertex1][vertex2]["weight"] = weight


def costs2attributes(G, cost, attr='weight'):
    """
    Convert a cost function to an edge attribute.
    """
    for a, b in G.edges():
        G[a][b][attr] = cost(a, b)


def dijkstra(graph, source, cost=lambda u, v: 1):
    """
    Compute shortest paths from the source vertex to all other vertices.
    """
    # Apply the cost function to graph edges as weights
    costs2attributes(graph, cost)

    # Use NetworkX's shortest_path function
    paths = nx.shortest_path(graph, source=source, weight='weight')

    # Sort the paths as lists of vertices
    return {target: paths[target] for target in paths}


def visualize(graph, view='dot', name='mygraph', nodecolors=None):
    """
    Visualize the graph using graphviz.
    """
    dot = Digraph(name=name, format=view)

    # Add nodes
    for node in graph.nodes:
        color = nodecolors.get(str(node), "white") if nodecolors else "white"
        dot.node(str(node), color=color, style="filled")

    # Add edges
    for edge in graph.edges:
        dot.edge(str(edge[0]), str(edge[1]))

    # Render graph
    dot.render(name, view=True)

def view_shortest(G, source, target, cost=lambda u, v: 1):
    path = dijkstra(G, source, cost)[target]
    print(path)
    colormap = {str(v): 'orange' for v in path}
    visualize(G, view='dot', nodecolors=colormap)



import unittest

class TestGraphs(unittest.TestCase):
    def setUp(self):
        self.graph = WeightedGraph([(1, 2), (2, 3), (3, 4)])
        self.graph.set_weight(1, 2, 10)
        self.graph.set_weight(2, 3, 5)
        self.graph.set_weight(3, 4, 1)

    def test_vertices_and_edges(self):
        self.assertIn(1, self.graph.vertices())
        self.assertIn((1, 2), self.graph.edges())

    def test_weights(self):
        self.assertEqual(self.graph.get_weight(1, 2), 10)
        self.assertEqual(self.graph.get_weight(2, 3), 5)

    def test_dijkstra(self):
        result = dijkstra(self.graph, 1, cost=lambda u, v: self.graph.get_weight(u, v))
        self.assertEqual(result[4], [1, 2, 3, 4])

if __name__ == "__main__":
    G = WeightedGraph([(1, 2), (2, 3), (3, 4)])
    G.set_weight(1, 2, 10)
    G.set_weight(2, 3, 5)
    G.set_weight(3, 4, 1)

    print("Shortest Paths:", dijkstra(G, 1, cost=lambda u, v: G.get_weight(u, v)))

    view_shortest(G, 1, 4, cost=lambda u, v: G.get_weight(u, v))

