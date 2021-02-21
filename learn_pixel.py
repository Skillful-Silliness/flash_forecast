import board
import time
import neopxiel

pixel_pin = board.D18
num_pixels = 36

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


