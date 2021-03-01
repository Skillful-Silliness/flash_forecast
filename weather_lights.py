import board
import neopixel
import time

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import RED, BLUE, GREEN

from weather import Weather

pixel_pin = board.D18
num_pixels = 263 #5m strip
ORDER = neopixel.GRB

COLOR_CONFIG = [
    {
        'color': BLUE,
        'temp': 0.0
    },
    {
        'color': GREEN,
        'temp': 50.0
    },
    {
        'color': RED,
        'temp': 100.0
    }
]

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

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

weather = Weather()
sparkle = None

while True:
    temp = weather.get_one_call_data().current.temperature()['temp']
    color = get_color(temp)

    old_temp = temp

    sparkle = sparkle if sparkle and temp == old_temp else Sparkle(pixels, speed=0.001, color=color)

    # print("Current temperature: ", temp)
    sparkle.animate()
