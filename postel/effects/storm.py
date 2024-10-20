"""
Efekt boure.

Na nahodnych mistech se objevuji bile "rozplizle" body, ktere
pomalu pohasinaji.
"""

import random

from postel import settings
from postel.neopixels import PIXELS
from postel.effects.shared import TEMPERATURE


SPARK_COOLING = 1.12
SPARK_SPARKLING = 20
SPARK_ROZLEZANI = 1.6


def init(step):
    global TEMPERATURE
    TEMPERATURE = [0 for i in range(settings.NUMBER_OF_LEDS)]


def step(step):
    # chladnuti
    for idx in range(settings.NUMBER_OF_LEDS):
        value = int(round(TEMPERATURE[idx] / SPARK_COOLING))
        if value > 255:
            value = 255
        elif value < 5:
            value = 0
        TEMPERATURE[idx] = value

    # rozlezani
    for flame_idx in range(0, settings.NUMBER_OF_LEDS-2):
        if TEMPERATURE[flame_idx] < TEMPERATURE[flame_idx+1]:
            TEMPERATURE[flame_idx] = int(round(TEMPERATURE[flame_idx+1] / SPARK_ROZLEZANI))

    for flame_idx in range(settings.NUMBER_OF_LEDS-1, 1, -1):
        if TEMPERATURE[flame_idx] < TEMPERATURE[flame_idx-1]:
            TEMPERATURE[flame_idx] = int(round(TEMPERATURE[flame_idx-1] / SPARK_ROZLEZANI))

    # sometimes new sparks appear in the flame
    if random.randint(0, 255) < int(SPARK_SPARKLING):
        y = random.randint(0, settings.NUMBER_OF_LEDS - 1)
        TEMPERATURE[y] = 255

    # transform heat map to colors
    for i in range(settings.NUMBER_OF_LEDS):
        PIXELS.set(i, (TEMPERATURE[i], TEMPERATURE[i], TEMPERATURE[i]))
