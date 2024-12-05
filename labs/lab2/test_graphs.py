import unittest
from graphs import Graph, WeightedGraph, dijkstra

class TestWeightedGraph(unittest.TestCase):
    def setUp(self):
        self.graph = WeightedGraph([('A', 'B', 1), ('B', 'C', 2)])

    def test_get_set_weight(self):
        # Test getting existing weight
        self.assertEqual(self.graph.get_weight('A', 'B'), 1)

        # Test updating weight
        self.graph.set_weight('A', 'B', 5)
        self.assertEqual(self.graph.get_weight('A', 'B'), 5)

        # Test default behavior for unweighted edge
        self.graph.add_edge('C', 'D')
        self.assertIsNone(self.graph.get_weight('C', 'D'))  # Updated expectation

    def test_add_edge_with_weight(self):
        self.graph.add_edge('C', 'D')
        self.graph.set_weight('C', 'D', 3)
        self.assertEqual(self.graph.get_weight('C', 'D'), 3)

class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.graph = WeightedGraph([('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 4)])

    def test_shortest_path_basic(self):
        # Test shortest path using weights
        paths = dijkstra(self.graph, 'A')
        self.assertEqual(paths['C'], ['A', 'B', 'C'])  # Correct path with minimum weight

    def test_cost_function(self):
        # Test custom cost function (uniform cost favors direct path)
        paths = dijkstra(self.graph, 'A', cost=lambda u, v: 1)
        self.assertEqual(paths['C'], ['A', 'C'])  # Direct path is shortest with uniform costs

    def test_disconnected_graph(self):
        # Add a disconnected node and ensure no path is found
        self.graph.add_vertex('D')
        paths = dijkstra(self.graph, 'A')
        self.assertNotIn('D', paths)

if __name__ == "__main__":
    unittest.main()
