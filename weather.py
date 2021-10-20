import os
import requests
from time import time
from dotenv import load_dotenv

load_dotenv()

DATA_EXPIRATION_SECS = 600

URL_ROOT = 'https://api.openweathermap.org/data/2.5'

PATHS = {
    "aqi": "air_pollution",
    "aqi_forecast": "air_pollution/forecast",
    "forecast_3h": "forecast"
}


class Weather:
    def __init__(self, lat=None, lon=None):
        self.api_key = os.getenv("OWM_API_KEY")
        self.lat = lat or float(os.getenv("WEATHERLIGHTS_LAT"))
        self.lon = lon or float(os.getenv("WEATHERLIGHTS_LON"))

        self.data = {
            "aqi": None,
            "aqi_forecast": None,
            "forecast_3h": None,
        }

        self.last_updated = {}

    def make_request(self, key):
        url = '%s/%s' % (URL_ROOT, PATHS[key])
        params = {"lat": self.lat, "lon": self.lon,
                  "appid": self.api_key, "units": "imperial"}

        return requests.get(url, params=params).json()

    def is_data_expired(self, key):
        return time() - self.last_updated[key] > DATA_EXPIRATION_SECS

    def set_last_updated(self, key):
        self.last_updated[key] = time()

    def get_data(self, key):
        if self.data[key] == None or self.is_data_expired(key):
            self.data[key] = self.make_request(key)
            self.set_last_updated(key)

        return self.data[key]

    def get_forecast_3h_data(self):
        return self.get_data("forecast_3h")["list"]

    def get_aqi_data(self):
        return self.get_data("aqi")["list"][0]["main"]["aqi"]

    def get_aqi_forecast_data(self):
        # TODO: refine further
        return self.get_data("aqi_forecast")["list"]


def demo():
    weather = Weather()

    forecast = weather.get_forecast_3h_data()
    aqi = weather.get_aqi_data()

    print(forecast)
    print(aqi)
