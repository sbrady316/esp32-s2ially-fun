# Tests for logger
from logger import Logger

log = Logger.Create()
log.Status("Something Important")
log.Log("Hello, World")
