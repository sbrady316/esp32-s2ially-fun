# Simple library for "logging" to the serial port via print
class Logger:
    """A simple class for logging via print"""
    _currentId = 0

    def Create():
        Logger._currentId = Logger._currentId + 1
        return Logger(Logger._currentId)


    def __init__(self, id: int):
        self._id = id


    def Status(self, status: str) -> None:
        header_length = 60
        status_length = 6 + len(status)
        self._Log('> ', f"{status} {'-' * max(0, header_length - status_length)}")


    def Log(self, message: str) -> None:
        self._Log('   ', message)

 
    def _Log(self, header: str, message: str) -> None:
        print(f'|{self._id}|{header}{message}')
