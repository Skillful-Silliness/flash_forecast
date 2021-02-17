import os
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

owm = OWM(os.getenv("OWM_API_KEY"))

t_lat = 39.324314
t_lon = -120.179020

mgr = owm.weather_manager()

td = mgr.weather_at_coords(t_lat, t_lon).weather.temperature('fahrenheit')
works = td['temp']


print(works)
