from redis import Redis
from pickle import loads, dumps

GLOBAL_NAMESPACE = "weatherlights"


INIT_STATE = {
    # controls
    "controls:lights_on": True,
    "controls:brightness": 0.1,

    # data
    "data:aqi_current": None,
    # "data:aqi_forecast": None,
    "data:weather_forecast_3h": None,
    "data:weather_current": None,

    #config
    # "config:lat": None,
    # "config:lon": None,
    # "config:owm_api_key": None,
}

print("initializing redis store...")

r = Redis()

def get_all():
    return get_keys(INIT_STATE.keys())

def get_keys(keys):
    values = list(map(loads, r.mget(keys)))

    return dict(zip(keys, values))

def get(key):
    if key in INIT_STATE and not r.exists(key):

        r.set(key, dumps(INIT_STATE.get(key)))

    return loads(r.get(key))


def set(key, val):
    r.set(key, dumps(val))
