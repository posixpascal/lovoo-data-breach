#!/usr/bin/env python
# -*- encoding: utf8 -*-
# Get a precise location of lovoo users

import http.client
import json

from geo import Geolocation, LocationMapper

MALE = 1
FEMALE = 2

R = 6378137


class DataEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class User(object):
    def __init__(self, payload):
        self.locations = []
        self.name = payload["name"]
        self.distance = payload["locations"]["current"]["distance"]
        self.id = payload["id"]
        self.last_online_time = payload["lastOnlineTime"]
        self.is_online = bool(payload["isOnline"])
        self.is_mobile = bool(payload["isMobile"])
        self.api_location = False
        self.payload = payload
        self.picture = self.picture_url()

    def picture_url(self):
        return "https://img.lovoo.com/users/pictures/{0}/image.jpg".format(self.payload["picture"])

class Lovoo(object):
    def __init__(self, options):
        latitude = float(options["location"]["latitude"])
        longitude = float(options["location"]["longitude"])

        if not latitude or not longitude:
            print("Please specify a latitude and longitude in lovoo.py (line 155)")
            raise SystemExit(0)

        self.location = Geolocation((latitude, longitude))

        self.target_gender = MALE
        self.radius = options["radius"]
        self.users = []
        pass

    def add_user(self, user):
        user.api_location = Geolocation(self.location)
        self.users.append(user)

    def scan(self, page = 1):
        connection = http.client.HTTPSConnection("www.lovoo.com")
        connection.request("GET", self.build_api_url(page))
        response = connection.getresponse()
        if response.status == 200:
            data = json.loads(response.read().decode('utf-8'))
            for user_payload in data["response"]["result"]:
                user = User(user_payload)
                self.add_user(user)


    def scan_area(self):
        page = 1
        print("[Lovoo]: Starting...")




        while page < 30:
            print("[Lovoo]: Querying page {0} / 30...".format(page))
            self.scan(page)

            latitude = self.location.offset_latitude(5)
            print("[Lovoo]:  up\t\t({0})".format(latitude))
            self.scan(page)

            latitude = self.location.offset_latitude(-10)
            print("[Lovoo]:  down\t\t({0})".format(latitude))
            self.scan(page)

            longitude = self.location.offset_longitude(5)
            print("[Lovoo]:  right\t\t({0})".format(longitude))
            self.scan(page)


            longitude = self.location.offset_longitude(-10)
            print("[Lovoo]:  left\t\t({0})".format(longitude))
            self.scan(page)

            # resetting geoposition
            self.location.offset_latitude(5)
            self.location.offset_longitude(5)
            print("[Lovoo]: Done - Next page...")

            page += 1

        print("[Lovoo]: All done. Dumping data to: data.json...")
        self.dump_data()
        print("[Lovoo]: Done dumping... Measuring...")
        self.measure()

    def dump_data(self):
        json.dump(self.users, open("data.json", "w"), cls = DataEncoder)


    def measure(self):
        data = json.load(open("data.json", "r"))

        # sort by user id
        sorted_data = {}
        for row in data:
            if row['id'] in sorted_data:
                sorted_data[row['id']].append(row)
            else:
                sorted_data[row['id']] = []

        parsed_user = {}
        for id, user_entries in sorted_data.items():
            lmapper = LocationMapper()
            for user in user_entries:
                location = Geolocation((user['api_location']['latitude'],
                                        user['api_location']['longitude']))
                lmapper.feed_location(location, float(user['distance']))

            parsed_user[id] = {
                "real_location": lmapper.triangulate(),
                "user": user_entries
            }

        json.dump(parsed_user, open("result.json", "w"), cls = DataEncoder)


    def build_api_url(self, page):
        return "/api_web.php/users?ageFrom=16\
&ageTo=26\
&gender=1\
&genderLooking={0}\
&isOnline=true\
&latitude={1}\
&longitude={2}\
&orderBy=distance\
&radiusTo={3}\
&resultPage={4}\
&type=env\
&userQuality[0]=pic".format(self.target_gender, str(self.location.latitude), str(self.location.longitude), self.radius, page)

if __name__ == "__main__":
    lovoo = Lovoo({
        "location": {
            "latitude": False,
            "longitude": False
        },
        "radius": 10
    })
    lovoo.scan_area()

