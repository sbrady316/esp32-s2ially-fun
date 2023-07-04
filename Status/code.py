import time
from adafruit_datetime import datetime

from logger import Logger
from time_sync import TimeSync
from label_display import LabelDisplay
from NetHelper import NetHelper


def GetHmsStr(time: datetime) -> str:
    """Formats the specified time as hour:minutes:seconds"""
    str = f'{time.hour:02}:{time.minute:02}:{time.second:02}'
    # print(f'GetHmsStr -> {str}')
    return str

def GetSecrets():
    """Get wifi details and more from a secrets.py file"""
    try:
        from secrets import secrets
    except ImportError:
        print("WiFi secrets are kept in secrets.py, please add them there!")
        raise

    return secrets


#######################################
#
# Init
#
DELAY_IN_SECONDS = 0.5

logger = Logger.Create()

logger.Status("=" * 40)
logger.Status(f'{"ESP32-S2 Adafruit IO Time test": ^40s}' )
logger.Status("=" * 40)

secrets = GetSecrets()

labelDisplay = LabelDisplay(Logger.Create())
netHelper = NetHelper(Logger.Create(), secrets["ssid"], secrets["password"])
timeSyncEngine = TimeSync(
    Logger.Create(), 
    netHelper.GetHttpSession(), 
    aio_username= secrets["aio_username"], 
    aio_key=secrets["aio_key"], 
    location=secrets.get("timezone", None))

#
# Sync time with outside world
#
timeSyncEngine.Sync()

#######################################
#
# Keep time, forever
#
while True:
    labelDisplay.SetText(
        GetHmsStr(
            datetime.now()))

    time.sleep(DELAY_IN_SECONDS)
