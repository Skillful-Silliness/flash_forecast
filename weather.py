import os
from dotenv import load_dotenv
from pyowm.owm import OWM

load_dotenv()

owm = OWM(os.getenv("OWM_API_KEY"))

# Truckee, CA
t_lat = 39.324314
t_lon = -120.179020

mgr = owm.weather_manager()

one_call = mgr.one_call(lat = t_lat, lon = t_lon, exclude='minutely', units='imperial')
humidity = one_call.current.humidity
temp = one_call.current.temperature()

print("Humidity:", humidity)
print("Temperature:", temp['temp'])

