import unittest
from graphs import Graph  # Import your graph implementation
from hypothesis import given, strategies as st

class TestGraphEdges(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge('A', 'B')

    def test_edges_and_vertices(self):
        for edge in self.graph.edges():
            a, b = edge
            self.assertIn(a, self.graph.vertices(), f"Vertex {a} not found in vertices after adding edge {edge}.")
            self.assertIn(b, self.graph.vertices(), f"Vertex {b} not found in vertices after adding edge {edge}.")

    def test_no_duplicate_edges(self):
        self.graph.add_edge('A', 'B')  # Add the same edge again
        edges = self.graph.edges()
        self.assertEqual(len(edges), 1, "Duplicate edges found in the graph.")

class TestGraphNeighbors(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_edge('A', 'B')

    def test_bidirectional_neighbors(self):
        neighbors_a = self.graph.neighbors('A')
        neighbors_b = self.graph.neighbors('B')

        self.assertIn('B', neighbors_a, "'B' not found as a neighbor of 'A'.")
        self.assertIn('A', neighbors_b, "'A' not found as a neighbor of 'B'.")

    def test_non_existent_vertex(self):
        with self.assertRaises(KeyError, msg="Accessing neighbors of a non-existent vertex did not raise KeyError."):
            self.graph.neighbors('NonExistent')

class TestGraphShortestPath(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('B', 'C')

    def test_shortest_path_symmetry(self):
        path_ab = self.graph.shortest_path('A', 'C')
        path_ba = self.graph.shortest_path('C', 'A')

        self.assertEqual(path_ab, path_ba[::-1], "Shortest path from A to C is not the reverse of C to A.")

    def test_large_graph(self):
        large_graph = Graph()
        for i in range(1000):
            large_graph.add_vertex(f"Node{i}")
        for i in range(999):
            large_graph.add_edge(f"Node{i}", f"Node{i+1}")

        self.assertEqual(len(large_graph.vertices()), 1000, "Vertex count mismatch in large graph.")
        self.assertEqual(len(large_graph.edges()), 999, "Edge count mismatch in large graph.")

# Hypothesis Tests
class TestGraphWithHypothesis(unittest.TestCase):
    @given(a=st.text(), b=st.text())
    def test_add_edge_vertices(self, a, b):
        graph = Graph()
        graph.add_edge(a, b)
        self.assertIn(a, graph.vertices(), f"Vertex {a} not found in vertices after adding edge ({a}, {b}).")
        self.assertIn(b, graph.vertices(), f"Vertex {b} not found in vertices after adding edge ({a}, {b}).")

if __name__ == "__main__":
    unittest.main()
