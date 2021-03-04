import board
import neopixel
import time

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

from weather import Weather

pixel_pin = board.D18
# num_pixels = 36  # small box
num_pixels = 14  # hours
# num_pixels = 263  # 5m strip
ORDER = neopixel.GRB

# COLOR_CONFIG = [
#     {
#         'color': PURPLE,
#         'temp': 0.0
#     },
#     {
#         'color': BLUE,
#         'temp': 32.0
#     },
#     {
#         'color': RED,
#         'temp': 55.0
#     },
#     {
#         'color': YELLOW,
#         'temp': 70.0
#     },
#     {
#         'color': RED,
#         'temp': 90.0
#     }
# ]

COLOR_CONFIG = [
    {
        hour: 1,
        led: 5.5
        # 'color': PURPLE,
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

DAY_STARTS = [0, 9, 18, 27]


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


def get_progress(lower, upper, current):
    return 0 if upper == lower else (current - lower) / (upper - lower)


def interpolate(lower, upper, progress):
    return (1 - progress) * lower + progress * upper


def interpolate_color_value(lower, upper, progress, idx):
    return round(interpolate(lower[idx], upper[idx], progress))


weather = Weather(lat=30.2672, lon=-97.7431)
sparkle = None

temp = 0

while True:
    with neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.25, auto_write=False, pixel_order=ORDER) as pixels:
        while True:
            for i in range(num_pixels):
                # TODO: fade between actual temp and feels like
                temp = weather.get_one_call_data().forecast_daily[i].temperature()[
                    'temp']
                pixels[i] = get_color(temp)
                # print("temperature: ", temp)

            pixels.show()
            # Solid(pixels, color).animate()
