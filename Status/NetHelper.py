# Helpers for getting online

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

from logger import Logger

class NetHelper:
    """Helper class for getting online and making http requests"""
    def __init__(self, logger: Logger, wifiId: str, wifiPassword: str) -> None:
        self._logger = logger

        logger.Log(f'Connecting to {wifiId}...')
        wifi.radio.connect(wifiId, wifiPassword)
        logger.Log(f"Connected to {wifiId} as {wifi.radio.ipv4_address}")

        ipv4 = ipaddress.ip_address("8.8.4.4")
        logger.Log("Ping google.com: %f ms" % wifi.radio.ping(ipv4))

        self._pool = socketpool.SocketPool(wifi.radio)

    def GetHttpSession(self):
        return adafruit_requests.Session(self._pool, ssl.create_default_context())
