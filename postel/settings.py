# credentials pro pripojeni k wifi
WIFI_SSID = '<change-me>'
WIFI_PASSWORD = '<change-me>'

# URL ridiciho serveru
URL = "http://192.168.89.5/postel/index.txt"

# TODO: tohle bude asi jinak...
# kazdy n-ty cyklus se provede HTTP request na server
SERVER_REQUEST_PERIOD = 40

# jak dlouho se bude cekat na odpoved ze serveru
REQUEST_TIMEOUT = 0.2

# jak dlouho trva prehravani jednoho efektu; v krocich
# EFFECT_DURATION = 1500
EFFECT_DURATION = 200

# jak dlouho trva setrvani ve tme behem 2 prechodu (po fade-out, pred fade-in); v krocich
FADE_WAIT_DURATION = 200

# maximalni jas LED diod (0..1)
MAX_BRIGHTNESS = 0.6

# po jakych prirustcich jasu probiha fade in/out
# BRIGHTNESS_STEP = 0.001
BRIGHTNESS_STEP = 0.01

# pin, na kterem je neopixel prouzek pripojen
LED_MAIN_GPIO = 4

# pocet diod v prouzku
NUMBER_OF_LEDS = 120




DEBUG = True
