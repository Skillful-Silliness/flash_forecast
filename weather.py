import os
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

owm = OWM(os.getenv("OWM_API_KEY"))
lat = float(os.getenv("WEATHERLIGHTS_LAT"))
lon = float(os.getenv("WEATHERLIGHTS_LON"))

mgr = owm.weather_manager()

one_call = mgr.one_call(lat=lat, lon=lon, exclude='minutely', units='imperial')
humidity = one_call.current.humidity
temp = one_call.current.temperature()

print("Humidity:", humidity)
print("Temperature:", temp['temp'])

