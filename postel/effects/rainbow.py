"""
Efekt duhy (plasmy).

Vykradeno z demoscen: https://lodev.org/cgtutor/plasma.html
"""

import math
from postel import settings
from postel.neopixels import PIXELS, hsv_to_rgb


# duha se generuje do 2D pole; aby to tak v plose vypadalo, je potreba
# aby kazdy prouzek mel hodnotu MOARE_Y unikatni, od 0 do 6
MOARE_Y = 0


def get_plasma_value(x, y):
    v = (
        128
        + (128 * math.sin(x / 16))
        + 128
        + (128 * math.sin(y / 8))
        + 128
        + (128 * math.sin((x + y) / 16))
        + 128
        + (128 * math.sin(math.sqrt(x * x + y * y))/8)
    )
    return int(round(v / 3))


def generate_plasma_pattern():
    out = []
    for x in range(settings.NUMBER_OF_LEDS):
        v = int(round(get_plasma_value(x, MOARE_Y)))
        out.append(v)
    return out


def generate_plasma_pallette():
    out = []
    for i in range(256):
        h = 65535 * i / 256
        out.append(hsv_to_rgb(h, 255, 255))
    return out


# rainbow efekt se generuje z predem vypocitaneho patternu a palety barev
PALLETTE = generate_plasma_pallette()
PATTERN = generate_plasma_pattern()


def init(step):
    pass


def step(step):
    b = []
    for idx, item in enumerate(PATTERN):
        color = PALLETTE[(item + step) % 256]
        PIXELS.set(idx, color)  # TODO: set_raw?
