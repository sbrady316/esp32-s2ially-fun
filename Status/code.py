import time
from adafruit_datetime import datetime
import rtc

import ipaddress
import ssl
import wifi
import socketpool
import displayio
import adafruit_requests
import secrets
import board
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font
import adafruit_requests
import digitalio


def PrintStatus(status: str) -> None:
    header_length = 40
    status_length = 3 + len(status)
    print(f'|- {status}', '-'*max(0, header_length - status_length))


def GetHmsStr(time: datetime) -> str:
    """Formats the specified time as hour:minutes:seconds"""
    str = f'{time.hour:02}:{time.minute:02}:{time.second:02}'
    # print(f'GetHmsStr -> {str}')
    return str


def GetAdafruitTime() -> datetime:
    """Gets the time from the ADA fruit time service"""
    PrintStatus("Time to get ill")
    print("Fetching text from", TIME_URL)
    response = requests.get(TIME_URL)
    timeText = response.text
    print(f"timeText is {timeText}")
    remoteTime = datetime.fromisoformat(timeText)
    print("-" * 40)

    return remoteTime

def SetLocalTime(now: datetime) -> None:
    PrintStatus(f"Setting real-time clock to {now.isoformat()}...")
    r = rtc.RTC()
    preAdjustment = datetime.now()
    r.datetime = now.timetuple()
    postAdjustment = datetime.now()
    print(f"Adjust time from local:{preAdjustment} to remote:{postAdjustment} -> diff:{(postAdjustment - preAdjustment).total_seconds()}s")
    print("-" * 40)

    

#######################################
#
# Init
#
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

# Get our username, key and desired timezone
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]
location = secrets.get("timezone", None)
TIME_URL = f'https://io.adafruit.com/api/v2/{aio_username}/integrations/time/clock?x-aio-key={aio_key}&tz={location}'

# Set up background image and text
display = board.DISPLAY
bitmap = displayio.OnDiskBitmap("/images/stars_background.bmp")
tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
group = displayio.Group()
group.append(tile_grid)
font = bitmap_font.load_font("/fonts/Arial-Bold-36.bdf")
text_area = bitmap_label.Label(font, color=0xFF0000)
text_area.x = 90
text_area.y = 90
group.append(text_area)
display.show(group)

print("Connecting to %s..."%secrets["ssid"])
wifi.radio.connect(secrets["ssid"], secrets["password"])
print("Connected to %s!"%secrets["ssid"])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % wifi.radio.ping(ipv4))

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

#
# Sync time with outside world
#
SetLocalTime(GetAdafruitTime())

#######################################
#
# Keep time, forever
#
while True:
    now = datetime.now()
    nowStr = GetHmsStr(now)
    if text_area.text != nowStr:
        if nowStr.endswith("00"):
            print(f"The current time is {nowStr}")
        text_area.text = nowStr
    time.sleep(DELAY_IN_SECONDS)
