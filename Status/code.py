import time
from adafruit_datetime import datetime
import rtc

from logger import Logger
from time_sync import TimeSync
from label_display import LabelDisplay

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import secrets

import displayio
import board
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font


def GetHmsStr(time: datetime) -> str:
    """Formats the specified time as hour:minutes:seconds"""
    str = f'{time.hour:02}:{time.minute:02}:{time.second:02}'
    # print(f'GetHmsStr -> {str}')
    return str


#######################################
#
# Init
#
logger = Logger.Create()

print("=" * 40)
print("ESP32-S2 Adafruit IO Time test")
print("=" * 40)

DELAY_IN_SECONDS = 0.5

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

labelDisplay = LabelDisplay(Logger.Create())

logger.Log(f'Connecting to {secrets["ssid"]}...')
wifi.radio.connect(secrets["ssid"], secrets["password"])
logger.Log("Connected to %s!" % secrets["ssid"])
logger.Log(f"My IP address is {wifi.radio.ipv4_address}")

ipv4 = ipaddress.ip_address("8.8.4.4")
logger.Log("Ping google.com: %f ms" % wifi.radio.ping(ipv4))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

#
# Sync time with outside world
#
syncEngine = TimeSync(
    Logger.Create(), 
    requests, 
    aio_username= secrets["aio_username"], 
    aio_key=secrets["aio_key"], 
    location=secrets.get("timezone", None))
syncEngine.Sync()

#######################################
#
# Keep time, forever
#
while True:
    labelDisplay.SetText(
        GetHmsStr(
            datetime.now()))

    time.sleep(DELAY_IN_SECONDS)
