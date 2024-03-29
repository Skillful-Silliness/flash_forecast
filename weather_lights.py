import board

import math
import neopixel
import random
import time

import webserver.state_store as state_store

from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

# from aqi import AQI
from weather import Weather
from color_config import * #TEMP_COLOR_CONFIG #AQI_COLOR_CONFIG

pixel_pin = board.D18
# num_pixels = 36  # small box
# num_pixels = 285  # test
# num_pixels = 14  # hours
# num_pixels = 263  # 5m strip
num_pixels = 450 # tree
ORDER = neopixel.GRB



def get_led_span(start, end):
    is_reversed = start > end

    led_range = reversed(range(end, start + 1)
                         ) if is_reversed else range(start, end + 1)
    return list(led_range)


AQI_SPANS = [
    get_led_span(61, 96)
]

WEATHER_DEMO_SPANS = [
    get_led_span(0, 60)
]

WEATHER_FORECAST_SPANS = [
    get_led_span(97, 299),
    get_led_span(300, 449)
]

TEST_SPANS = []


class SparklePixel:
    def __init__(self, min_duration, max_duration, target_color):
        now = time.time()

        self.target_color = target_color
        self.duration = random.randrange(min_duration, max_duration) / 1000
        self.start_time = now
        self.end_time = now + self.duration
        self.freq_coef = 2 * math.pi / self.duration

    def get_progress(self):
        elapsed = time.time() - self.start_time
        return -0.5 * math.cos(self.freq_coef * elapsed) + 0.5

    def get_color(self, original_color):
        return interpolate_colors(original_color, self.target_color, self.get_progress())


class SparkleAnimation:
    def __init__(self, key, min_duration, max_duration, target_color):
        self.current_pixels = {}
        self.key = key
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.target_color = target_color

    def refresh(self, weather_objs):

        now = time.time()


        # keep only non-expired pixels
        self.current_pixels = {
            key: pixels for key, pixels in self.current_pixels.items() if now < pixels.end_time}

        statuses = list(map(get_status_from_weather, weather_objs))
        indexes = []

        for index, status in enumerate(statuses):
            if status.lower() == self.key.lower():
                indexes.append(index)

        if len(indexes) > 0:
            new_pixel_idx = random.choice(indexes)

            if not new_pixel_idx in self.current_pixels:
                self.current_pixels[new_pixel_idx] = SparklePixel(
                    self.min_duration, self.max_duration, self.target_color)

    def apply(self, idx, original_color):
        if not idx in self.current_pixels:
            return original_color

        return self.current_pixels[idx].get_color(original_color)


rain_animation = SparkleAnimation("rain", 250, 750, BLUE)
snow_animation = SparkleAnimation("snow", 250, 500, WHITE)

rain_demo_animation = SparkleAnimation("rain", 250, 750, BLUE)
snow_demo_animation = SparkleAnimation("snow", 250, 500, WHITE)

def get_dummy_weather(temp):
    key = "rain" if temp > 32 else "snow"
    return {"weather": [{"main": key}], "temp": temp}

def fill_weather_demo_span(pixels, led_span):
    num_leds = len(led_span)

    dummy_weather_objs = []

    for index, led in enumerate(led_span):
        temp = interpolate(0, 100, index / num_leds) 
        dummy_weather_objs.append(get_dummy_weather(temp))

    rain_demo_animation.refresh(dummy_weather_objs)
    snow_demo_animation.refresh(dummy_weather_objs)

    for index, led in enumerate(led_span):
        temp_color = get_color_from_temp(dummy_weather_objs[index]["temp"])
        color = rain_demo_animation.apply(index, snow_demo_animation.apply(index, temp_color))

        pixels[led] = color
    
    
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

        pixels[led] = interpolate_colors(prev_color, next_color, progress)


def fill_aqi_span(pixels, led_span, aqi):
    color = get_color_from_aqi(aqi)

    for index, led in enumerate(led_span):
        pixels[led] = color


def fill_weather_forecast_span(pixels, led_span, weather_objs):
    forecast_temps = list(map(get_temp_from_weather, weather_objs))

    forecasts_per_led = len(forecast_temps) / len(led_span)

    blanks = {}

    rain_animation.refresh(weather_objs)
    snow_animation.refresh(weather_objs)

    for index, led in enumerate(led_span):
        forecast_pos = index * forecasts_per_led

        prev_idx = math.floor(forecast_pos)
        next_idx = min(math.ceil(forecast_pos), len(forecast_temps) - 1)

        t = weather_objs[prev_idx]["dt_txt"] if "dt_txt" in weather_objs[prev_idx] else ""

        if ("12:00:00" in t or "00:00:00" in t) and t not in blanks:
            blanks[t] = True
            pixels[led] = BLACK
            continue

        prev_temp = forecast_temps[prev_idx]
        next_temp = forecast_temps[next_idx]

        prev_color_original = get_color_from_temp(prev_temp)
        next_color_original = get_color_from_temp(next_temp)

        prev_color = snow_animation.apply(prev_idx,
                                          rain_animation.apply(prev_idx, prev_color_original))
        next_color = snow_animation.apply(next_idx,
                                          rain_animation.apply(next_idx, next_color_original))

        # take only the fractional component
        progress = math.modf(forecast_pos)[0]

        pixels[led] = interpolate_colors(prev_color, next_color, progress)


def get_color_bounds(value, key, config):
    for i in range(len(config)):
        current = config[i]

        if value < current[key]:
            prev = config[i - 1] or current
            return [prev, current]

    # fallback: value is greater than max in config
    last = config[len(config) - 1]
    return [last, last]


def get_color_from_aqi(aqi):
    lower, upper, progress = get_color_interpolation_args(
        aqi, 'aqi', AQI_COLOR_CONFIG)

    return interpolate_colors(lower['color'], upper['color'], progress)


def get_color_from_temp(temp):
    lower, upper, progress = get_color_interpolation_args(
        temp, 'temp', TEMP_COLOR_CONFIG)

    return interpolate_colors(lower['color'], upper['color'], progress)


def get_color_interpolation_args(value, key, config):
    lower, upper = get_color_bounds(value, key, config)
    return [lower, upper, get_progress(lower[key], upper[key], value)]


def get_status_from_weather(weather):
    return weather["weather"][0]["main"]


def get_temp_from_weather(weather):
    return weather['main']['temp']


def get_progress(lower, upper, current):
    return 0 if upper == lower else (current - lower) / (upper - lower)


def interpolate(lower, upper, progress):
    return (1 - progress) * lower + progress * upper


def interpolate_colors(start_color, end_color, progress):
    return [interpolate_color_component(start_color, end_color, progress, idx) for idx in (0, 1, 2)]


def interpolate_color_component(lower, upper, progress, idx):
    return round(interpolate(lower[idx], upper[idx], progress))


def render_pixels(pixels):
    try:
        data = weather.refresh_all()

        pixels.brightness = state_store.get("controls:brightness")

        # make a copy, then prepend current weather to forecast
        forecast_objs = data["weather_forecast_3h"][:]
        forecast_objs.insert(0, data["weather_current"])

        for forcast_span in WEATHER_FORECAST_SPANS:
            fill_weather_forecast_span(pixels, forcast_span, forecast_objs)

        for aqi_span in AQI_SPANS:
            fill_aqi_span(pixels, aqi_span, data["aqi_current"])

        for test_span in TEST_SPANS:
            fill_test_span(pixels, test_span)

        for weather_demo_span in WEATHER_DEMO_SPANS:
            fill_weather_demo_span(pixels, weather_demo_span)

        pixels.show()
    except Exception as e:
        print(e)


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
        if state_store.get("controls:lights_on"):
            render_pixels(pixels)
        else:
            render_off(pixels)
