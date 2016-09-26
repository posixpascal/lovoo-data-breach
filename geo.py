from math import pi, cos

R = 6378137

class LocationMapper(object):
    def __init__(self):
        self.locations = []
        pass

    def feed_location(self, location, distance):
        self.locations.append((location, distance))

    def triangulate(self):
        closest_points = []
        print("triangulate points here (geo.py / line 15)")


class Geolocation(object):
    def __init__(self, location):
        if isinstance(location, Geolocation):
            self.latitude = location.latitude
            self.longitude = location.longitude
        else:
            self.latitude = location[0]
            self.longitude = location[1]

    def offset_latitude(self, meters):
        dlat = meters / R
        self.latitude = self.latitude + dlat * 180 / pi
        return self.latitude

    def offset_longitude(self, meters):
        dlng = meters / (R * cos(pi * self.latitude / 180))
        self.longitude = self.longitude + dlng * 180 / pi
        return self.longitude