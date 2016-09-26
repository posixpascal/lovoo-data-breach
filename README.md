# Lovoo - Private Data Leak

This repository contains scripts to gather the location of any lovoo user (approx. 10meters difference) without having
to register an independent account. This script exploits an *public* API route.

This api route returns a JSON response of users near a given location, a typical user response will contain
the following data:

```json
{
    "_type": "user",
    "id": "XXXXXXX",
    "name": "XXXXXXX",
    "gender": 1,
    "age": 27,
    "lastOnlineTime": 1474896338,
    "whazzup": "",
    "freetext": "XXXXXXX",
    "isInfluencer": 0,
    "flirtInterests": [ ],
    "options": {
        "profileShareable": 1
    },
    "isVip": 0,
    "counts": {
        "p": 4,
        "m": 8
    },
    "locations": {
        "home": {
            "city": "XXXXXXXX",
            "country": "DE",
            "distance": 4.4
        },
        "current": {
            "city": "XXXXX",
            "country": "DE",
            "distance": 4.4
        }
    },
    "mutualHashtagCount": 0,
    "isNew": 0,
    "isOnline": 0,
    "isMobile": 0,
    "isHighlighted": 0,
    "picture": "XXXX",
    "images": [
        {
            "url": "https://img.lovoo.com/users/pictures/XXXXX/thumb_l.jpg",
            "width": 160,
            "height": 160
        },
        {
        "url": "https://img.lovoo.com/users/pictures/XXXXX/image.jpg",
        "width": 958,
        "height": 1280
        }
    ],
    "isVerified": 0,
    "verifications": {
        "facebook": 0,
        "verified": 0,
        "confirmed": 1
    }
   }
```



The interesting part of this response is the fact that you can specify any location and the users distance is calculated
by the lat/lng you speicified. In the example above you can see that the user is 4.4kilometres away from my pseudo
location. With this data you can basically triangulate a user with no more than 7 queries to the lovoo API.

Other things exposed by this API:
- locations
- images (public)
- facebook user
- lastOnlineTime
- username
- gender
- relationship status

If you are authenticated you can also get the following:
- profile "matches" - this is a lovoo-thing I don't know.
- flirt interests

You may run this script using the lovoo.py (this is also available as a module)

```
python lovoo.py
```

This script starts with a preset location and then checks subsequent api responses in nearby locations.
You can get even higher accuracy by providing more samples.

The **geo.py#LocationMapper** does the calculation where the user currently is. The implementation is left blank intentionally
because I don't want to encourage abuse of this API.

After the script succeeded you can view the saved locations (on a per-user basis) in the **data.json** file.

## Contribution
I don't want any feature contribution

## License
License = WTFPL

## Status
Working as of 26.09.2016

Submitted to golem.de on September 26th for further investigation - no response yet. :x