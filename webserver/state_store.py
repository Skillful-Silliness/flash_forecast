from redis import Redis
from pickle import loads, dumps

DEFAULTS = {
    "lightson": True,
    "brightness": 0.1,
}

print("initializing redis store...")
r = Redis()


def get_all():
    keys = DEFAULTS.keys()
    values = list(map(loads, r.mget(keys)))

    return dict(zip(keys, values))


def get(key):
    if key in DEFAULTS and not r.exists(key):
        r.set(key, dumps(DEFAULTS.get(key)))

    return loads(r.get(key))


def set(key, val):
    r.set(key, dumps(val))
