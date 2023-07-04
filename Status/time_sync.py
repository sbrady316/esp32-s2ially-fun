import time
from adafruit_datetime import datetime
import rtc

from logger import Logger

import adafruit_requests
import secrets

class TimeSync:
    """Class to sync the local clock with a remote source"""

    def __init__(self, logger: Logger, requests, aio_username: str, aio_key: str, location: str):
        self._logger = logger
        self._requests = requests
        self._baseUrl = f'https://io.adafruit.com/api/v2/{aio_username}/integrations/time/clock'
        self._timeUrl = self._baseUrl + f'?x-aio-key={aio_key}&tz={location}'


    def Sync(self):
        remoteTime = self._GetAdafruitTime()
        self._SetLocalTime(remoteTime)


    def _GetAdafruitTime(self) -> datetime:
        """Gets the time from the ADA fruit time service"""
        self._logger.Status("Time to get ill")
        self._logger.Log(f"Fetching text from {self._baseUrl}...")
        response = self._requests.get(self._timeUrl)
        timeText = response.text
        self._logger.Log(f"timeText is {timeText}")
        remoteTime = datetime.fromisoformat(timeText)
        self._logger.Log("-" * 40)

        return remoteTime


    def _SetLocalTime(self, now: datetime) -> None:
        self._logger.Status(f"Setting real-time clock to {now.isoformat()}...")
        r = rtc.RTC()
        preAdjustment = datetime.now()
        r.datetime = now.timetuple()
        postAdjustment = datetime.now()
        self._logger.Log(f"Adjust time from local:{preAdjustment} to remote:{postAdjustment} -> diff:{(postAdjustment - preAdjustment).total_seconds()}s")
        self._logger.Log("-" * 40)

