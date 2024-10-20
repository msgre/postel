import utime

from postel import states
from postel import commands
from postel import settings
from postel.effects import fire, rainbow, storm, water
from postel.neopixels import PIXELS
from postel.wifi import connect_wifi


# TODO: najit nejakou optimalni hodnotu SLEEP; vypsat si jak dlouho (v sec) trvaly jednotlive efekty a udelat z toho nejaky prumer
SLEEP = 5 # TODO:


# globalni promenne ridici animace
effect_idx = None
transition = None
transition_state = None
brightness = None
step = None
step_memory = None
init = None
fn = None
last_command_ts = None


def reset_animation(idx=0, transition_=True):
    global effect_idx
    global transition
    global transition_state
    global brightness
    global step
    global step_memory
    global init
    global fn

    effect_idx = idx
    if transition_:
        transition = True
        transition_state = states.STATE_FADE_IN
        brightness = 0
    else:
        transition = False
        brightness = settings.MAX_BRIGHTNESS
    PIXELS.set_brightness(brightness)
    step = 0
    step_memory = 0

    init, fn = EFFECTS[effect_idx]
    init(step)
    PIXELS.show()


# podporovane efekty
EFFECTS = [
    (rainbow.init, rainbow.step),
    (water.init, water.step),
    (storm.init, storm.step),
    (fire.init, fire.step),
]

# --------------------------------------------------------

# inicializace animace
reset_animation(0)
# TODO: nejaka vizualizace return hodnoty
connect_wifi(settings.WIFI_SSID, settings.WIFI_PASSWORD)

# hlavni smycka animace
while True:
    if transition:
        # prechody
        if transition_state == states.STATE_FADE_IN:
            # rozjasnovani efektu z cerne do finalni podoby
            brightness = brightness + settings.BRIGHTNESS_STEP
            if brightness >= settings.MAX_BRIGHTNESS:
                if settings.DEBUG:
                    print(f'Fade-in skoncil, nyni bude probihat plne efekt {effect_idx}')
                transition = False
                brightness = settings.MAX_BRIGHTNESS
                step_memory = step + settings.EFFECT_DURATION

        elif transition_state == states.STATE_FADE_OUT:
            # ztmavovani efektu do cerne
            brightness = brightness - settings.BRIGHTNESS_STEP
            if brightness <= 0:
                if settings.DEBUG:
                    print(f'Fade-out skoncil, nyni nastane tma')
                brightness = 0
                effect_idx = (effect_idx + 1) % 4
                init, fn = EFFECTS[effect_idx]
                init(step)
                transition_state = states.STATE_FADE_WAIT
                step_memory = step + settings.FADE_WAIT_DURATION
        
        else:
            # cekacka v cerne
            utime.sleep_ms(SLEEP)

            if step > step_memory:
                # cekacka v cerne skoncila, pojdme odkryt dalsi efekt
                if settings.DEBUG:
                    print(f'Tma skoncila, nastava fade-in')
                transition_state = states.STATE_FADE_IN
                step = 0

#             # TODO: docasne vyrazeno
#             elif 0 and step % settings.SERVER_REQUEST_PERIOD == 0:
#                 # jsme stale v cerne, pojdme se syncnout se serverem
#                 r = urequests.get(settings.URL, timeout=settings.REQUEST_TIMEOUT)
#                 if r.status_code == 200:
#                     cmd, parameters, ts = r.content.decode().split('\n')
#                     if ts > last_command_ts:
#                         # command se od posledniho requestu zmenil, pojdme jej zpracovat
#                         if settings.DEBUG:
#                             print('Command changed, lets process it')
#                         last_command_ts = ts
#                         parameters = parameters.split(':')
#                         if settings.DEBUG:
#                             print(f'Commad parameters: {parameters}')
# 
#                         # ukonceni aktualniho efektu (stahnutim do cerne)
#                         if cmd == commands.CMD_END_EFFECT:
#                             if settings.DEBUG:
#                                 print('End effect')
#                             transition_state = states.STATE_FADE_OUT
# 
#                         # probuzeni z cerne do efektu
#                         elif cmd == commands.CMD_NEXT_EFFECT:
#                             if settings.DEBUG:
#                                 print('Next effect')
#                             transition_state = states.STATE_FADE_IN
#                             step = 0
# 
#                         # okamzite prepnuti na konkretni efekt
#                         elif cmd == commands.CMD_SET_EFFECT:
#                             if settings.DEBUG:
#                                 print('Set effect')
#                             # TODO:
#                             # reset_animation(idx, bool(parameters[1]))
# 
#                         elif cmd == CMD_CONFIGURATION:
#                             # jemne nastaveni konfiguracnich parametru
#                             pass
#                 r.close()

        # probiha prechod, upravme aktualni hodnotu jasu
        PIXELS.set_brightness(brightness)
    
    elif step > step_memory:
        # doba pro plny efekt se vycerpala, jdeme efekt utlumit
        if settings.DEBUG:
            print('Efekt skoncil, nastava jeho utlumeni pres fade-out')
        transition = True
        transition_state = states.STATE_FADE_OUT
    
    # efekt
    fn(step)
    PIXELS.show()
    step += 1
