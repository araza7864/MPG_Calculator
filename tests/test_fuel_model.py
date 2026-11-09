import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "mpg_trip"))
from mpg_calculator import estimated_mpg, highway_weight

class FuelModelTests(unittest.TestCase):
    def test_speed_thresholds(self):
        for speed, expected in [(0, .15), (24.9, .15), (25, .40), (40, .70), (55, .85)]:
            with self.subTest(speed=speed):
                self.assertEqual(highway_weight(speed), expected)

    def test_fuel_consumption_weighting(self):
        self.assertAlmostEqual(estimated_mpg(.5, 20, 40), 100 / (50/20 + 50/40))
        self.assertEqual(estimated_mpg(0, 20, 40), 20)
        self.assertEqual(estimated_mpg(1, 20, 40), 40)
