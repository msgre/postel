import utime
import network
import urequests
from postel import settings


def connect_wifi(ssid, password, max_wait=15):
    """
    Pripojeni k wifine.

    Vrati True pokud se pripojeni povedlo, False kdyz ne.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)

    # Wait for connect or fail
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        if settings.DEBUG:
            print('Waiting for connection...')
        utime.sleep_ms(1000)

    # Handle connection error
    if wlan.status() != 3:
        if settings.DEBUG:
            print('Network connection failed')
        return False

    if settings.DEBUG:
        print('Connected')
    status = wlan.ifconfig()
    if settings.DEBUG:
        print('ip = ' + status[0])
    return True
