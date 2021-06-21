from rendash.plugins import BasePlugin
from rendash.config import current_config
from rendash.utils.text import draw_text

from typing import Union
from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock



class TextDisplay(BasePlugin):
    def __init__(
        self,
        text: str,
        font: Font = None,
        color_bg: Color = None,
        color_fg: Color = None,
        center: bool = True,
        padding: int = 8,
    ):
        """Display a given string.
    
        If any of the `font`, `color_bg`, or `color_fg` parameters are None,
        the values from ``current_config`` are used.
        """

        self.text = text
        self.font = font or current_config.font
        self.color_bg = color_bg or current_config.color_bg
        self.color_fg = color_fg or current_config.color_fg
        self.center = center
        self.padding = padding

    def render(self, surface: Surface, clock: Clock):
        surface.fill(self.color_bg)

        draw_rect = Rect(
            self.padding,
            self.padding,
            surface.get_width() - self.padding,
            surface.get_height() - self.padding,
        )

        draw_text(self.text, surface, draw_rect, self.font, self.color_fg, center=self.center)


class BoolDisplay(BasePlugin):
    def __init__(
        self,
        value: Union[bool, None],
        prefix: str,
        font: Font = None,
        text_true: str = "YES",
        text_false: str = "NO",
        text_none: str = "unknown",
        color_bg_true: Color = None,
        color_bg_false: Color = None,
        color_bg_none: Color = None,
        color_fg: Color = None,
        multi_line: bool = False,
        center: bool = True,
        padding: int = 8,
    ):
        """Display a given boolean, with a text prefix.
    
        This is technically tri-state - True and False are valid values, which
        are treated as below, but None is also a valid value. Any value that
        is not explicitly True or False is treated as if it was None.

        If the boolean is True, `color_bg_true` is used as the background, and
        `text_true` is displayed (which defaults to "YES").

        If the boolean is False, `color_bg_false` is used as the background,
        and `text_false` is displayed (which defaults to "NO").

        If the value is set to None, `color_bg_none` is used as the background,
        and `text_none` is displayed (which defaults to "unknown").

        If the `multi_line` parameter is True, then the `prefix` is displayed
        on a line above the `text_true` or `text_false` parameter, otherwise
        it is displayed on the same line.

        If the `font` parameter is None, the value from ``current_config`` is
        used.
        """

        self.value = value
        self.prefix = prefix
        self.font = font or current_config.font
        self.text_true = text_true
        self.text_false = text_false
        self.text_none = text_none
        self.color_bg_true = color_bg_true or current_config.color_bg
        self.color_bg_false = color_bg_false or current_config.color_bg
        self.color_bg_none = color_bg_none or current_config.color_bg
        self.color_fg = color_fg or current_config.color_fg
        self.multi_line = multi_line
        self.center = center
        self.padding = padding

    def render(self, surface: Surface, clock: Clock):
        if self.value == True:
            value = self.text_true
            surface.fill(self.color_bg_true)
        elif self.value == False:
            value = self.text_false
            surface.fill(self.color_bg_false)
        else:
            value = self.text_none
            surface.fill(self.color_bg_none)

        draw_rect = Rect(
            self.padding,
            self.padding,
            surface.get_width() - self.padding,
            surface.get_height() - self.padding,
        )

        text = [self.prefix, value]
        if not self.multi_line:
            text = " ".join(text)

        draw_text(text, surface, draw_rect, self.font, self.color_fg, center=self.center)
