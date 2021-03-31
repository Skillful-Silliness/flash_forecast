import board
import neopixel
import time
import math

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

from weather import Weather

pixel_pin = board.D18
num_pixels = 36  # small box
# num_pixels = 14  # hours
# num_pixels = 263  # 5m strip
ORDER = neopixel.GRB


def get_led_span(start, end):
    is_reversed = start > end

    led_range = reversed(range(end, start + 1)
                         ) if is_reversed else range(start, end + 1)
    return list(led_range)


FORECAST_SPANS = [get_led_span(17, 9), get_led_span(26, 34)]

COLOR_CONFIG = [
    {
        'color': PURPLE,
        'temp': 0.0
    },
    {
        'color': BLUE,
        'temp': 32.0
    },
    {
        'color': AQUA,
        'temp': 55.0
    },
    {
        'color': YELLOW,
        'temp': 70.0
    },
    {
        'color': RED,
        'temp': 90.0
    }
]


def fill_led_span(pixels, led_span, weather_objs):
    forecast_temps = list(map(get_temp_from_weather, weather_objs))

    forecasts_per_led = len(forecast_temps) / len(led_span)

    for index, led in enumerate(led_span):
        print("led: ", led)
        forecast_pos = index * forecasts_per_led

        # TODO: clamp to make sure no overflow?
        prev_temp = forecast_temps[math.floor(forecast_pos)]
        next_temp = forecast_temps[math.ceil(forecast_pos)]

        progress = math.modf(forecast_pos)[0]

        temp = interpolate(prev_temp, next_temp, progress)

        pixels[led] = get_color(temp)


def get_bounds(temp):
    for i in range(len(COLOR_CONFIG)):
        current = COLOR_CONFIG[i]

        if temp < current['temp']:
            prev = COLOR_CONFIG[i - 1] or current
            return [prev, current]

    # fallback: temp is greater than max in config
    last = COLOR_CONFIG[len(COLOR_CONFIG) - 1]
    return [last, last]


def get_color(temp):
    lower, upper, progress = get_interpolation_args(temp)

    return [interpolate_color_value(lower['color'], upper['color'], progress, idx) for idx in (0, 1, 2)]


def get_interpolation_args(temp):
    lower, upper = get_bounds(temp)
    return [lower, upper, get_progress(lower['temp'], upper['temp'], temp)]


def get_temp_from_weather(weather):
    return weather.temperature('fahrenheit')['temp']


def get_progress(lower, upper, current):
    return 0 if upper == lower else (current - lower) / (upper - lower)


def interpolate(lower, upper, progress):
    return (1 - progress) * lower + progress * upper


def interpolate_color_value(lower, upper, progress, idx):
    return round(interpolate(lower[idx], upper[idx], progress))


weather = Weather()

with neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.25, auto_write=False, pixel_order=ORDER) as pixels:
    while True:
        weather_objs = weather.get_forecast_3h_data().forecast.weathers

        for led_span in FORECAST_SPANS:
            fill_led_span(pixels, led_span, weather_objs)

        pixels.show()
