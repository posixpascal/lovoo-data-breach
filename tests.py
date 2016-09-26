import unittest

from geo import Geolocation
from lovoo import Lovoo

class TestStringMethods(unittest.TestCase):

    def test_geolocation(self):
        latitude = 38.0951425
        longitude = 8.607229
        location = Geolocation((latitude, longitude))
        location.offset_latitude(-1000)
        self.assertEqual(location.latitude, 38.086159347158805)

        location.offset_longitude(1000)
        self.assertEqual(location.longitude, 8.618642206510954)

    def test_lovoo(self):
        pass

if __name__ == '__main__':
    unittest.main()
