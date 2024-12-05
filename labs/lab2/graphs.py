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
        super().__init__()
        self.weights = {}

        # Add edges and weights
        for edge in edgelist:
            if len(edge) == 3:  # Edge with a weight
                self.add_edge(edge[0], edge[1])
                self.set_weight(edge[0], edge[1], edge[2])
            elif len(edge) == 2:  # Edge without a weight
                self.add_edge(edge[0], edge[1])

    def get_weight(self, vertex1, vertex2):
        """
        Get the weight of the edge between vertex1 and vertex2.
        Return None if no weight exists.
        """
        return self[vertex1][vertex2].get("weight", None) if self.has_edge(vertex1, vertex2) else None

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


def dijkstra(graph, source, cost=None):
    """
    Compute shortest paths from the source vertex to all other vertices.
    """
    # Apply the cost function to all edges
    for u, v in graph.edges():
        graph[u][v]['weight'] = cost(u, v) if cost else graph.get_weight(u, v)

    # Compute shortest paths using NetworkX
    paths = nx.shortest_path(graph, source=source, weight='weight')

    return {target: paths[target] for target in paths}



def visualize(graph, view='dot', name='mygraph', nodecolors=None, edgecolors=None, edgelabels=None):
    """
    Visualize the graph using graphviz.

    Parameters:
    - graph: The graph object to visualize.
    - view: The output format (e.g., 'pdf', 'png').
    - name: The output filename.
    - nodecolors: Dictionary mapping nodes to colors.
    - edgecolors: Dictionary mapping edges to colors.
    - edgelabels: Dictionary mapping edges to labels.
    """
    dot = Digraph(name=name, format=view)

    # Add nodes with optional coloring
    for node in graph.nodes:
        color = nodecolors.get(str(node), "white") if nodecolors else "white"
        dot.node(str(node), color=color, style="filled")

    # Add edges with optional coloring and labels
    for edge in graph.edges:
        edge_color = edgecolors.get((str(edge[0]), str(edge[1])), "black") if edgecolors else "black"
        label = edgelabels.get((str(edge[0]), str(edge[1])), "") if edgelabels else ""
        dot.edge(str(edge[0]), str(edge[1]), color=edge_color, label=label)

    # Render graph
    dot.render(name, view=False)
    print(f"Graph saved as {name}.gv")


class TestGraph:
    def __init__(self):
        """
        Placeholder for tests that validate the functionality of the Graph class.
        """
        pass

    def test_vertices(self):
        """
        Test adding and retrieving vertices.
        """
        graph = Graph()
        graph.add_vertex('A')
        assert 'A' in graph.vertices()

    def test_edges(self):
        """
        Test adding and retrieving edges.
        """
        graph = Graph()
        graph.add_edge('A', 'B')
        assert ('A', 'B') in graph.edges()

    def test_dijkstra(self):
        """
        Test the Dijkstra shortest path implementation.
        """
        graph = WeightedGraph([('A', 'B', 1), ('B', 'C', 2)])
        paths = dijkstra(graph, 'A')
        assert paths['C'] == ['A', 'B', 'C']


if __name__ == "__main__":
    # Create an example graph for testing
    graph = WeightedGraph([('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 4)])

    # Test vertices and edges
    print("Vertices:", graph.vertices())
    print("Edges:", graph.edges())

    # Test Dijkstra's algorithm
    shortest_paths = dijkstra(graph, 'A')
    print("Shortest paths from A:", shortest_paths)

    # Visualize the graph with custom colors
    node_colors = {'A': 'red', 'B': 'blue', 'C': 'green'}
    edge_colors = {('A', 'B'): 'blue', ('B', 'C'): 'green'}
    edge_labels = {('A', 'B'): '1', ('B', 'C'): '2', ('A', 'C'): '4'}
    visualize(graph, nodecolors=node_colors, edgecolors=edge_colors, edgelabels=edge_labels)
