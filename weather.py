import os
from time import time
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

DATA_EXPIRATION_SECS = 60


class Weather:
    def __init__(self, lat=None, lon=None):
        owm = OWM(os.getenv("OWM_API_KEY"))

        self.lat = lat or float(os.getenv("WEATHERLIGHTS_LAT"))
        self.lon = lon or float(os.getenv("WEATHERLIGHTS_LON"))

        self.mgr = owm.weather_manager()
        self.one_call_data = None
        self.forecast_3h_data = None
        self.last_updated = {}

    def is_data_expired(self, key):
        return time() - self.last_updated[key] > DATA_EXPIRATION_SECS

    def set_last_updated(self, key):
        self.last_updated[key] = time()

    def get_one_call_data(self):
        if self.one_call_data == None or self.is_data_expired("one_call"):
            self.one_call_data = self.mgr.one_call(
                lat=self.lat, lon=self.lon, exclude='minutely', units='imperial')
            self.set_last_updated("one_call")

        return self.one_call_data

    def get_forecast_3h_data(self):
        if self.forecast_3h_data == None or self.is_data_expired("forecast_3h"):
            self.forecast_3h_data = self.mgr.forecast_at_coords(
                self.lat, self.lon, "3h")
            self.set_last_updated("forecast_3h")

        return self.forecast_3h_data

    def go(self):
        return self.get_one_call_data()


def demo():
    weather = Weather()
    one_call_data = weather.get_one_call_data()

    humidity = one_call_data.current.humidity
    temp = one_call_data.current.temperature()

    print("Humidity:", humidity)
    print("Temperature:", temp['temp'])

    forecast = weather.get_forecast_3h_data()
    for item in forecast.forecast:
        print(item.reference_time('iso'), item.temperature('fahrenheit'))
