import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src' / 'mpg_trip'))
import main
import route_service
from vehicle_service import choose_from_menu


class TripWorkflowTests(unittest.TestCase):
    def test_demo_generates_map_payload(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(main, 'MAP_DIR', temp):
            main.demo()
            data = json.loads((Path(temp) / 'route.json').read_text())
            self.assertTrue(data['demo'])
            self.assertEqual(data['geojson']['features'][0]['geometry']['type'], 'LineString')
            self.assertGreater(data['summary']['estimated_mpg'], 24)
            self.assertLess(data['summary']['estimated_mpg'], 34)

    def test_trip_writes_output_independent_of_working_directory(self):
        geojson = {'type': 'FeatureCollection', 'features': []}
        with tempfile.TemporaryDirectory() as temp, patch.object(main, 'MAP_DIR', temp), \
             patch.object(main, 'ORS_API_KEY', 'synthetic-test-key'), \
             patch('builtins.input', side_effect=['Demo A', 'Demo B']), \
             patch.object(main, 'get_coordinates', side_effect=[(1, 2, 'Demo A'), (3, 4, 'Demo B')]), \
             patch.object(main, 'get_directions', return_value=(16093.44, 1200, geojson)), \
             patch.object(main, 'get_vehicle_mpg', return_value=(20, 30)):
            main.main()
            data = json.loads((Path(temp) / 'route.json').read_text())
            self.assertAlmostEqual(data['summary']['distance_miles'], 10, places=4)
            self.assertEqual(data['origin'], 'Demo A')
            self.assertEqual(data['geojson'], geojson)

    def test_empty_vehicle_options_have_a_clear_error(self):
        with self.assertRaisesRegex(ValueError, 'No vehicle options'):
            choose_from_menu([], 'Select vehicle')

    def test_geocoder_handles_empty_results(self):
        response = Mock()
        response.json.return_value = {'features': []}
        with patch.object(route_service.requests, 'get', return_value=response):
            with self.assertRaisesRegex(ValueError, 'Address not found'):
                route_service.get_coordinates('Synthetic unknown address')
