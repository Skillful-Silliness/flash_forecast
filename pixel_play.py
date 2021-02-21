# PIXEL PLAY

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
#num_pixels = 263 #5m strip
num_pixels = 36 #small box

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

#pixels[0] = (10, 0, 0)
#pixels[10] = (0, 10, 0)
#pixels.show()
#RESET
#pixels.fill((0,0,0))

RED = 0x100000 # (0x10, 0, 0) also works

while True:
    with neopixel.NeoPixel(pixel_pin, num_pixels, auto_write=False, brightness=0.1) as pixels:
        #pixels[::5] = [RED] * (len(pixels) // 2)
        pixels[0] = (255, 0, 0)
        pixels[1] = (0, 255, 0)
        pixels[2] = (0, 0, 255)
        pixels.show()
        time.sleep(0.5)

        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(0.25)

        for i in range(num_pixels):
            if i % 2 == 0:
                pixels[i] = (255, 0, 0)
            if i % 3 == 0:
                pixels[i] = (0, 255, 0)
            if i % 5 == 0:
                pixels[i] = (0, 0, 255)
        pixels.show()
        time.sleep(1)


        print(len(pixels))

#def wheel(pos):
#    # Input a value 0 to 255 to get a color value.
#    # The colours are a transition r - g - b - back to r.
#    if pos < 0 or pos > 255:
#        r = g = b = 0
#    elif pos < 85:
#        r = int(pos * 3)
#       # g = 0
#        g = int(255 - pos * 3)
#        b = 0
#    elif pos < 170:
#        pos -= 85
#        r = int(255 - pos * 3)
#        g = 0
#        b = int(pos * 3)
#    else:
#        pos -= 170
#        r = 0
#        g = int(pos * 3)
#       # g = 0
#        b = int(255 - pos * 3)
#    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)
#

#def rainbow_cycle():
#    for i in range(num_pixels):
#        #pixel_index = (i * 256 // num_pixels) + j
#        pixels[i] = (i * 5, 5 * i , 50)
#            #pixels[i] = wheel(pixel_index & 255)
#        pixels.show()
#
#
#while True:
#    # Comment this line out if you have RGBW/GRBW NeoPixels
#   # pixels.fill((255, 66, 0))
#    # Uncomment this line if you have RGBW/GRBW NeoPixels
#    # pixels.fill((255, 0, 0, 0))
#   # pixels.show()
#   # time.sleep(1)
#
#    # Comment this line out if you have RGBW/GRBW NeoPixels
#   # pixels.fill((0, 255, 0))
#    # Uncomment this line if you have RGBW/GRBW NeoPixels
#    # pixels.fill((0, 255, 0, 0))
#   # pixels.show(
#    # Comment this line out if you have RGBW/GRBW NeoPixels
#   # pixels.fill((0, 0, 255))
#    rainbow_cycle()
#   #rainbow_cycle(0.0001)  # rainbow cycle with 1ms delay per step
