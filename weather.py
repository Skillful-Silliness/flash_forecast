import os
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

owm = OWM(os.getenv("OWM_API_KEY"))

t_lat = 39.324314
t_lon = -120.179020

mgr = owm.weather_manager()

# this gives an array of pyowm.weatherapi25.weather objects https://pyowm.readthedocs.io/en/latest/_modules/pyowm/weatherapi25/weather.html
forecast = mgr.one_call(lat=t_lat, lon=t_lon).forecast_daily


def get_temp(weather):
    return weather.temperature('fahrenheit')


temps = map(get_temp, forecast)

print(list(temps))
