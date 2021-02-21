import os
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

owm = OWM(os.getenv("OWM_API_KEY"))

t_lat = 39.324314
t_lon = -120.179020

mgr = owm.weather_manager()
one_call = mgr.one_call(lat=t_lat, lon=t_lon)


def get_temp(weather):
    return weather.temperature('fahrenheit')


temps = map(get_temp, one_call.forecast_daily)

print(list(temps))
