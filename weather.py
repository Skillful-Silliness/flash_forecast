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

    def is_data_expired(self):
        return time() - self.last_updated > DATA_EXPIRATION_SECS

    def get_one_call_data(self):
        if self.one_call_data == None or self.is_data_expired():
            self.one_call_data = self.mgr.one_call(lat=self.lat, lon=self.lon, exclude='minutely', units='imperial')
            self.last_updated = time()

        return self.one_call_data

def demo():
    weather = Weather()
    one_call_data = weather.get_one_call_data()

    humidity = one_call_data.current.humidity
    temp = one_call_data.current.temperature()

    print("Humidity:", humidity)
    print("Temperature:", temp['temp'])
