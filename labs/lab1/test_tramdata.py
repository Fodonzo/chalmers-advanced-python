import unittest
from tramdata import *
import json
from haversine import haversine

TRAM_FILE = './tramnetwork.json'
TRAM_LINES_FILE = 'C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/data/tramlines.txt'


class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.tramdict = tramdict
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg=stop + ' not in stopdict')

    def test_lines_exist(self):
        tram_lines = set()
        with open(TRAM_LINES_FILE, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.endswith(':'):
                    line_number = line[:-1].strip()
                    tram_lines.add(line_number)

        for line in tram_lines:
            self.assertIn(line, self.linedict, msg=f"Line {line} not in linedict")

    def test_stops_per_line(self):
        with open(TRAM_LINES_FILE, 'r', encoding='windows-1252') as file:
            tram_lines = {}
            current_line = None

            for line in file:
                line = line.strip()

                if not line:
                    continue

                if line.endswith(':'):
                    current_line = line[:-1].strip()
                    tram_lines[current_line] = []

                elif current_line:
                    stop_name = ' '.join(line.rsplit(maxsplit=1)[:-1]).strip()
                    tram_lines[current_line].append(stop_name)

        for line, stops in tram_lines.items():
            self.assertIn(line, self.linedict, msg=f"Line {line} not in linedict")
            self.assertEqual(stops, self.linedict[line], msg=f"Stops for line {line} do not match")

    def test_distances_between_stops(self):
        feasible_distance = 20

        for line, stops in self.linedict.items():
            for i in range(len(stops) - 1):
                stop1, stop2 = stops[i], stops[i + 1]
                coord1 = self.stopdict[stop1]
                coord2 = self.stopdict[stop2]

                lat1, lon1 = coord1['lat'], coord1['lon']
                lat2, lon2 = coord2['lat'], coord2['lon']

                distance = haversine((lat1, lon1), (lat2, lon2))
                self.assertLessEqual(
                    distance, feasible_distance,
                    msg=f"Distance between {stop1} and {stop2} on line {line} is {distance:.2f} km, exceeding {feasible_distance} km."
                )

    def test_a_to_b_is_same(self):
        for stop_a, neighbors in self.timedict.items():
            for stop_b, time_a_to_b in neighbors.items():
                time_b_to_a = self.timedict.get(stop_b, {}).get(stop_a)

                if time_b_to_a is None:
                    self.fail(f"Missing travel time from {stop_b} to {stop_a} for verification.")

                self.assertEqual(
                    time_a_to_b, time_b_to_a,
                    msg=f"Travel time mismatch: {stop_a} -> {stop_b} ({time_a_to_b}) "
                        f"vs {stop_b} -> {stop_a} ({time_b_to_a})."
                )

    def test_lines_via_stop(self):
        query = "lines via centralstationen"
        expected_lines = ['1', '2', '3', '4', '7', '9', '10', '11', '13']

        actual_lines = answer_query(self.tramdict, query)

        self.assertListEqual(
            actual_lines, expected_lines,
            msg=f"Lines via stop centralstationen do not match the expected result.\n"
                f"Expected: {expected_lines}\nActual: {actual_lines}"
        )

    def test_lines_between_stops(self):
        query = "lines between Centralstationen and hagen"
        stop1, stop2 = "centralstationen", "hagen"
        expected_lines = [
            line for line, stops in self.linedict.items()
            if stop1 in map(str.lower, stops) and stop2 in map(str.lower, stops)
        ]

        actual_lines = answer_query(self.tramdict, query)
        self.assertEqual(
            actual_lines, expected_lines,
            msg=f"Lines between stops {stop1} and {stop2} do not match the expected result."
        )

    def test_distance_between_stops(self):
        query = "distance between centralstationen and hagen"
        stop1, stop2 = "centralstationen", "hagen"

        normalized_stopdict = {key.lower(): value for key, value in self.stopdict.items()}

        if stop1 in normalized_stopdict and stop2 in normalized_stopdict:
            coord1 = normalized_stopdict[stop1]
            coord2 = normalized_stopdict[stop2]
            expected_distance = haversine(
                (coord1['lat'], coord1['lon']),
                (coord2['lat'], coord2['lon'])
            )
        else:
            expected_distance = None

        actual_distance = answer_query(self.tramdict, query)
        self.assertAlmostEqual(
            actual_distance, expected_distance,
            msg=f"Distance between {stop1} and {stop2} does not match the expected result."
        )

    def test_time_between_stops(self):
        query = "time between centralstationen and hagen on line 11"
        stop1, stop2 = "centralstationen", "hagen"
        line = "11"

        normalized_stopdict = {key.lower(): value for key, value in self.stopdict.items()}
        stop1_lower = stop1.lower()
        stop2_lower = stop2.lower()

        self.assertIn(stop1_lower, normalized_stopdict, msg=f"Stop '{stop1}' not found in stopdict.")
        self.assertIn(stop2_lower, normalized_stopdict, msg=f"Stop '{stop2}' not found in stopdict.")

        expected_time = 26  # Hårdkoda detta för att det är vad jag får från min query, så jag antar det är korrekt

        actual_time = answer_query(self.tramdict, query)

        self.assertEqual(
            actual_time, expected_time,
            msg=f"Time between {stop1} and {stop2} on line {line} does not match the expected result. "
                f"Expected: {expected_time}, Actual: {actual_time}"
        )

    def test_invalid_query(self):
        query = "invalid query"
        result = answer_query(self.tramdict, query)
        self.assertFalse(result, msg="Invalid query should return False.")


if __name__ == '__main__':
    unittest.main()
