import board
import math
import neopixel
import random
import time

import webserver.state_store as state_store

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

from weather import Weather
from color_config import COLOR_CONFIG

pixel_pin = board.D18
# num_pixels = 36  # small box
num_pixels = 285  # test
# num_pixels = 14  # hours
# num_pixels = 263  # 5m strip
ORDER = neopixel.GRB


def get_led_span(start, end):
    is_reversed = start > end

    led_range = reversed(range(end, start + 1)
                         ) if is_reversed else range(start, end + 1)
    return list(led_range)


FORECAST_SPANS = [
    # get_led_span(0, 51),
    get_led_span(52, 142),
    # get_led_span(194, 143),
    get_led_span(284, 195)
]

TEST_SPANS = [
    get_led_span(0, 51),
    # get_led_span(52, 142),
    get_led_span(194, 143),
    # get_led_span(284, 195)
]


class RainPixel:
    def __init__(self):
        now = time.time()

        self.duration = random.randrange(250, 750) / 1000
        self.start_time = now
        self.end_time = now + self.duration
        self.freq_coef = 2 * math.pi / self.duration

    def get_progress(self):
        elapsed = time.time() - self.start_time
        return -0.5 * math.cos(self.freq_coef * elapsed) + 0.5

    def get_color(self, original_color):
        return [interpolate_color_value(
            original_color, BLUE, self.get_progress(), idx) for idx in (0, 1, 2)]


class RainAnimation:
    def __init__(self):
        self.current_pixels = {}

    def refresh(self, weather_objs):
        now = time.time()

        # keep only non-expired rain pixels
        self.current_pixels = {
            key: rain_pixel for key, rain_pixel in self.current_pixels.items() if now < rain_pixel.end_time}

        # get new sparkle pixel
        statuses = list(map(lambda weather: weather.status, weather_objs))

        rain_indexes = []

        for index, status in enumerate(statuses):
            if status.lower() == "rain":
                rain_indexes.append(index)

        if len(rain_indexes) > 0:
            new_pixel_idx = random.choice(rain_indexes)
            if not new_pixel_idx in self.current_pixels:
                self.current_pixels[new_pixel_idx] = RainPixel()

    def apply(self, idx, original_color):
        if not idx in self.current_pixels:
            return original_color

        return self.current_pixels[idx].get_color(original_color)


rain_animation = RainAnimation()


class SparkleAnimation:
    def __init__(self):
        self.next_sparkle_time = 0
        self.current_sparkles = {}

    def get_snow_sparkles(self, weather_objs):
        now = time.time()

        # keep only non-expired sparkles
        self.current_sparkles = {
            key: sparkle_end for key, sparkle_end in self.current_sparkles.items() if now < sparkle_end}

        if now > self.next_sparkle_time:
            self.next_sparkle_time = now + random.randrange(20, 250) / 1000

            # get new sparkle pixel
            statuses = list(map(lambda weather: weather.status, weather_objs))

            snow_indexes = []

            for index, status in enumerate(statuses):
                if status.lower() == "rain":
                    snow_indexes.append(index)

            if len(snow_indexes) > 0:
                new_sparkle_idx = random.choice(snow_indexes)
                self.current_sparkles[new_sparkle_idx] = time.time() + 0.05

        return self.current_sparkles


sparkle_animation = SparkleAnimation()


def fill_test_span(pixels, led_span):
    test_temps = list(range(0, 101))

    per_led = len(test_temps) / len(led_span)

    for index, led in enumerate(led_span):
        pos = index * per_led

        # TODO: clamp to make sure no overflow?
        prev_idx = math.floor(pos)
        next_idx = min(math.ceil(pos), len(test_temps) - 1)

        prev_temp = test_temps[prev_idx]
        next_temp = test_temps[next_idx]

        progress = math.modf(pos)[0]

        prev_color = get_color_from_temp(prev_temp)
        next_color = get_color_from_temp(next_temp)

        pixels[led] = [interpolate_color_value(
            prev_color, next_color, progress, idx) for idx in (0, 1, 2)]


def fill_led_span(pixels, led_span, weather_objs):
    forecast_temps = list(map(get_temp_from_weather, weather_objs))

    forecasts_per_led = len(forecast_temps) / len(led_span)

    # current_sparkles = sparkle_animation.get_snow_sparkles(weather_objs)
    rain_animation.refresh(weather_objs)

    for index, led in enumerate(led_span):
        forecast_pos = index * forecasts_per_led

        # TODO: clamp to make sure no overflow?
        prev_idx = math.floor(forecast_pos)
        next_idx = min(math.ceil(forecast_pos), len(forecast_temps) - 1)

        prev_temp = forecast_temps[prev_idx]
        next_temp = forecast_temps[next_idx]

        prev_color_original = get_color_from_temp(prev_temp)
        next_color_original = get_color_from_temp(next_temp)

        prev_color = rain_animation.apply(prev_idx, prev_color_original)
        next_color = rain_animation.apply(next_idx, next_color_original)

        progress = math.modf(forecast_pos)[0]

        pixels[led] = [interpolate_color_value(
            prev_color, next_color, progress, idx) for idx in (0, 1, 2)]


def get_color_bounds(temp):
    for i in range(len(COLOR_CONFIG)):
        current = COLOR_CONFIG[i]

        if temp < current['temp']:
            prev = COLOR_CONFIG[i - 1] or current
            return [prev, current]

    # fallback: temp is greater than max in config
    last = COLOR_CONFIG[len(COLOR_CONFIG) - 1]
    return [last, last]


def get_color_from_temp(temp):
    lower, upper, progress = get_color_interpolation_args(temp)

    return [interpolate_color_value(lower['color'], upper['color'], progress, idx) for idx in (0, 1, 2)]


def get_color_interpolation_args(temp):
    lower, upper = get_color_bounds(temp)
    return [lower, upper, get_progress(lower['temp'], upper['temp'], temp)]


def get_status_from_weather(weather):
    return weather.status


def get_temp_from_weather(weather):
    return weather.temperature('fahrenheit')['temp']


def get_progress(lower, upper, current):
    return 0 if upper == lower else (current - lower) / (upper - lower)


def interpolate(lower, upper, progress):
    return (1 - progress) * lower + progress * upper


def interpolate_color_value(lower, upper, progress, idx):
    return round(interpolate(lower[idx], upper[idx], progress))


def render_pixels(pixels):
    weather_objs = weather.get_forecast_3h_data().forecast.weathers

    pixels.brightness = 1.0  # state_store.get("brightness")

    for forcast_span in FORECAST_SPANS:
        fill_led_span(pixels, forcast_span, weather_objs)

    for test_span in TEST_SPANS:
        fill_test_span(pixels, test_span)

    pixels.show()


def render_off(pixels):
    pixels.fill(0)
    pixels.show()


print("initializing weather...")
weather = Weather()

print("starting lights...")

with neopixel.NeoPixel(
    pixel_pin, num_pixels, auto_write=False, pixel_order=ORDER
) as pixels:
    while True:
        if state_store.get("lightson"):
            render_pixels(pixels)
        else:
            render_off(pixels)
