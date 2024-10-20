import array
import rp2
import machine
from postel import settings


@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24,
)
def ws2812():
    """
    Obecna PIO rutina pro komunikaci s NeoPixelama.

    Viz https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-python-sdk.pdf,
    kapitola "3.9.2. WS2812 LED (NeoPixel)".
    """
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1).side(0)[T3 - 1]
    jmp(not_x, "do_zero").side(1)[T1 - 1]
    jmp("bitloop").side(1)[T2 - 1]
    label("do_zero")
    nop().side(0)[T2 - 1]
    wrap()


def hsv_to_rgb(hue, sat, val):
    """
    Prevede HSV na RGB. hue=0..65535, sat=0..255, val=0..255.

    V online kalkulackach je hue ve stupnich, sat/val v procentech. Musi se proto prepocitat:
        hue = 65536/360 * uhel
        sat = 255/100 * sat
        hue = 255/100 * hue

    Reimplementace funkcionality z https://github.com/adafruit/Adafruit_NeoPixel/blob/master/Adafruit_NeoPixel.cpp
    """
    hue = int(round(hue))
    sat = int(round(sat))
    if hue >= 65536:
        hue %= 65536

    hue = (hue * 1530 + 32768) // 65536
    if hue < 510:
        b = 0
        if hue < 255:
            r = 255
            g = hue
        else:
            r = 510 - hue
            g = 255
    elif hue < 1020:
        r = 0
        if hue < 765:
            g = 255
            b = hue - 510
        else:
            g = 1020 - hue
            b = 255
    elif hue < 1530:
        g = 0
        if hue < 1275:
            r = hue - 1020
            b = 255
        else:
            r = 255
            b = 1530 - hue
    else:
        r = 255
        g = 0
        b = 0

    v1 = int(round(1 + val))
    s1 = 1 + sat
    s2 = 255 - sat

    r = ((((r * s1) >> 8) + s2) * v1) >> 8
    g = ((((g * s1) >> 8) + s2) * v1) >> 8
    b = ((((b * s1) >> 8) + s2) * v1) >> 8

    return r, g, b


class NeopixelStrip:
    """
    Pomocna trida pro ovladani Neopixelu.
    """

    def __init__(self, gpio, count, sm_id, brightness=0.2):
        self.count = count
        self.brightness = brightness
        self.sm = rp2.StateMachine(
            sm_id, ws2812, freq=8_000_000, sideset_base=machine.Pin(gpio)
        )
        self.sm.active(1)
        self.array = array.array("I", [0 for _ in range(count)])

    def set(self, i, color):
        """
        Nastavi konkretni diodu "i" na zadanou barvu (r, g, b).

        Interne se (r, g, b) tupple prepocita na 24 bitovou hodnotu.
        """
        self.array[i] = (color[1] << 16) + (color[0] << 8) + color[2]

    def set_raw(self, i, raw_color):
        """
        Nastavi konkretni diodu "i" na zadanou barvu raw_color (24 bitova hodnota).
        """
        self.array[i] = raw_color

    def fill(self, color):
        """
        Nastavi cely prouzek na barvu (r, g, b).
        """
        val = (color[1] << 16) + (color[0] << 8) + color[2]
        for i in range(self.count):
            self.array[i] = val

    def show(self):
        """
        Preklopi interni pole do Neopixel prouzku (show se musi volat na konci kazdeho cyklu).
        """
        dimmer_ar = array.array("I", [0 for _ in range(self.count)])
        for i, c in enumerate(self.array):
            r = int(((c >> 8) & 0xFF) * self.brightness)
            g = int(((c >> 16) & 0xFF) * self.brightness)
            b = int((c & 0xFF) * self.brightness)
            dimmer_ar[i] = (g << 16) + (r << 8) + b
        state = machine.disable_irq()
        self.sm.put(dimmer_ar, 8)
        machine.enable_irq(state)

    def set_brightness(self, value):
        """
        Nastavi jas diod.

        Pri kazdem volani .show(), kdyz se preklapi hodnoty z interniho pole do diod,
        je vysledna RGB barva prepoctena s pouzitim hodnoty brightness.
        """
        self.brightness = value

    def copy(self, from_i, to_i):
        """
        Prekopiruje prvek z indexu from_i na pozivi to_i.
        """
        self.array[to_i] = self.array[from_i]



PIXELS = NeopixelStrip(
    # TODO: 1?
    settings.LED_MAIN_GPIO, settings.NUMBER_OF_LEDS, 1, brightness=settings.MAX_BRIGHTNESS
)
PIXELS.fill((0, 0, 0))
PIXELS.show()