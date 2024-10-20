"""
Efekt vody.

Na pasku interferuji 2 modre sinusovky, napodobuje to
vlneni hladiny vody.
"""

import math
from postel import settings
from postel.neopixels import PIXELS


def get_water_value(t):
    value = int(round(
        128 + (128 * math.sin(t / 17)) +
        128 + (128 * math.sin(math.sqrt(t*t) / 7))
    ) / 2)

    if value < 0:
        return 0
    elif value > 255:
        return 255
    return value


def init(step):
    for i in range(settings.NUMBER_OF_LEDS):
        value = get_water_value(i + step)
        PIXELS.set(i, (value//12, value//6, value))


def step(step):
    # shift
    for i in range(1, settings.NUMBER_OF_LEDS):
        PIXELS.copy(i, i-1)

    # vypocet nove hodnoty
    i = settings.NUMBER_OF_LEDS - 1
    value = get_water_value(i + step)
    PIXELS.set(i, (value//12, value//6, value))
