"""
Efekt ohne.

Vykradly efekt z ˇhttps://github.com/FastLED/FastLED/blob/master/examples/Fire2012/Fire2012.ino.
"""

import random
from postel import settings
from postel.neopixels import PIXELS
from postel.effects.shared import TEMPERATURE


# ohen se generuje po blocich o LEDS_PER_FLAME diodach, pricemz 
# je to zarizeno tak, ze sude bloky "hori" doleva a liche doprava,
# tj. na prouzku to vypada, jako by tam bylo NUMBER_OF_FLAMES/2
# plamenu, ktere plapolaji
# POZOR! nasledujici 2 parametry musi sedet k NUMBER_OF_LEDS
# konkretne NUMBER_OF_LEDS == LEDS_PER_FLAME * NUMBER_OF_FLAMES
LEDS_PER_FLAME = 15
NUMBER_OF_FLAMES = 8

# jak moc se ohen ochlazuje; cim vetsi cislo, tim vice se ochlazuje a mene zhne
COOLING = 17

# jak moc casto se objevuji jiskricky [0-255]; cim vetsi cislo, tim casteji
SPARKLING = 30

# teplota nahodne vznikle jiskry bude mezi temito 2 hodnotami
SPARKLING_MIN_TEMPERATURE = 160
SPARKLING_MAX_TEMPERATURE = 220

# jiskra vznikne pobliz stredu ohne, vzdalena o nahodnou hodnotu mezi 0 a touto konstantou
RANDOM_SPARK_POSITION = 3


def scale8_video(value, scale):
    return (int(value) * scale) >> 8 + (1 if int(value) & scale else 0)


def get_heat_color(heat):
    t192 = scale8_video(heat, 192)
    heatramp = t192 & 0x3f      # 0..63
    heatramp = heatramp << 2    # scale up to 0..252

    if t192 & 0x80:
        out = (255, 255, heatramp)
    elif t192 & 0x40:
        out = (255, heatramp, 0)
    else:
        out = (heatramp, 0, 0)

    return out


def init(step):
    global TEMPERATURE
    TEMPERATURE = [0 for i in range(settings.NUMBER_OF_LEDS)]


def step(step):
    global TEMPERATURE
    global PIXELS

    # cooldown of flame
    for idx in range(settings.NUMBER_OF_LEDS):
        value = TEMPERATURE[idx] - ((abs(int(COOLING)) << 3) >> 3) + 2
        if value > 255:
            value = 255
        elif value < 0:
            value = 0
        TEMPERATURE[idx] = value

    for flame_idx in range(NUMBER_OF_FLAMES):
        flame_type = flame_idx % 2
        if flame_type == 1:
            base_idx = flame_idx * LEDS_PER_FLAME
        else:
            base_idx = (flame_idx + 1) * LEDS_PER_FLAME - 1

        # heated particles move up
        if flame_type == 1:
            for i in range(LEDS_PER_FLAME - 1, 1, -1):
                y = i + base_idx
                TEMPERATURE[y] = (TEMPERATURE[y-1] + TEMPERATURE[y-2] + TEMPERATURE[y-2]) // 3

            y -= 1
            TEMPERATURE[y] = TEMPERATURE[y-1]
        else:
            for i in range(LEDS_PER_FLAME - 1, 1, -1):
                y = base_idx - i
                TEMPERATURE[y] = (TEMPERATURE[y+1] + TEMPERATURE[y+2] + TEMPERATURE[y+2]) // 3

            y += 1
            TEMPERATURE[y] = TEMPERATURE[y+1]

        # sometimes new sparks appear in the flame
        if random.randint(0, 255) < int(SPARKLING):
            spark_position = random.randint(0, RANDOM_SPARK_POSITION)
            if flame_type == 1:
                y = base_idx + spark_position
            else:
                y = base_idx - spark_position
            _temp = TEMPERATURE[y] + random.randint(SPARKLING_MIN_TEMPERATURE, SPARKLING_MAX_TEMPERATURE)
            if _temp > 255:
                _temp = 255
            TEMPERATURE[y] = _temp
            if spark_position == 0:
                if flame_type == 1:
                    TEMPERATURE[y-1] = _temp - random.randint(4, 20)
                else:
                    TEMPERATURE[y+1] = _temp - random.randint(4, 20)

    # transform heat map to colors
    for i in range(settings.NUMBER_OF_LEDS):
        PIXELS.set(i, get_heat_color(TEMPERATURE[i]))
