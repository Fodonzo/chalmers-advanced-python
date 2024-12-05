import unittest
from trams import TramNetwork, build_tram_network

class TestTramNetwork(unittest.TestCase):
    def setUp(self):
        # Build the tram network using the provided JSON
        self.network = build_tram_network("tramnetwork.json")

    def test_list_all_stops(self):
        stops = self.network.list_all_stops()
        self.assertIn("Centralstationen", stops)
        self.assertGreater(len(stops), 0)  # Ensure stops are loaded

    def test_list_all_lines(self):
        lines = self.network.list_all_lines()
        self.assertIn("Line 1", lines)
        self.assertGreater(len(lines), 0)  # Ensure lines are loaded

    def test_lines_via_stop(self):
        # Test for a stop with known lines
        lines = self.network.lines_via_stop("Centralstationen")
        self.assertIn("Line 1", lines)
        self.assertGreater(len(lines), 0)

    def test_lines_between_stops(self):
        # Test for stops with direct line connections
        lines = self.network.lines_between_stops("Centralstationen", "Brunnsparken")
        self.assertGreater(len(lines), 0)

    def test_invalid_stop(self):
        # Test for a stop not in the network
        with self.assertRaises(KeyError):
            self.network.lines_via_stop("NonExistentStop")

    def test_time_between_stops(self):
        # Validate time computation between connected stops
        time = self.network.time_between_stops("Centralstationen", "Brunnsparken")
        self.assertGreater(time, 0)

if __name__ == "__main__":
    unittest.main()
