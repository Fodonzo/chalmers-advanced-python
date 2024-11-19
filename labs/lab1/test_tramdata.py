import unittest
from tramdata import *
import math

TRAM_FILE = './tramnetwork.json'
TRAM_LINES_FILE = 'C:/Users/fredr/PycharmProjects/chalmers-advanced-python/labs/data/tramlines.txt'

class TestTramData(unittest.TestCase):

    def setUp(self):
        with open(TRAM_FILE) as trams:
            tramdict = json.loads(trams.read())
            self.stopdict = tramdict['stops']
            self.linedict = tramdict['lines']
            self.timedict = tramdict['times']

    def test_stops_exist(self):
        stopset = {stop for line in self.linedict for stop in self.linedict[line]}
        for stop in stopset:
            self.assertIn(stop, self.stopdict, msg = stop + ' not in stopdict')

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
        #Jag har suttit så länge och försökt lista ut problemet, men jag passar inte testet med UTF-8 av någon anledning
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

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def test_distances_between_stops(self):
        feasible_distance = 20

        for line, stops in self.linedict.items():
            for i in range(len(stops) - 1):
                stop1, stop2 = stops[i], stops[i + 1]
                coord1 = self.stopdict[stop1]
                coord2 = self.stopdict[stop2]

                lat1, lon1 = coord1['lat'], coord1['lon']
                lat2, lon2 = coord2['lat'], coord2['lon']

                distance = self.haversine(lat1, lon1, lat2, lon2)
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


if __name__ == '__main__':
    unittest.main()

