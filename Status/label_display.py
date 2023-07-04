import displayio
import board
from adafruit_display_text import bitmap_label
from adafruit_bitmap_font import bitmap_font

from logger import Logger

class LabelDisplay:
    """Class for displaying a label on the screen"""

    def __init__(self, logger: Logger):
        self._logger = logger

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

        self._label = text_area


    def SetText(self, text: str) -> None:
        if self._label.text != text:
            if (not self._label.text) or (text.endswith("00")):
                self._logger.Log(f"Updating label to {text}")
            self._label.text = text
