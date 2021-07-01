from collections.abc import Callable

from rendash.config import current_config
from rendash.plugins.basics import TextDisplay, BoolDisplay

from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock

import time
import requests


class HTTPTextDisplay(TextDisplay):
    def __init__(
        self,
        url: str,
        parser: Callable[..., str],
        cache_timeout: int = 300,
        font: Font = None,
        color_bg: Color = None,
        color_fg: Color = None,
        center: bool = True,
        padding: int = 8,
    ):
        """Displays text from the given ``url``, parsed by the ``parser``
        callable before display.

        Results are cached for ``cache_timeout`` seconds.

        Other parameters are the same as ``rendash.plugins.basics.TextDisplay``
        """

        super(HTTPTextDisplay, self).__init__(
            f"Waiting for HTTP refresh",
            font,
            color_bg,
            color_fg,
            center,
            padding,
        )

        self.http_url = url
        self.http_parser = parser
        self.cache_timeout = cache_timeout
        self.cache_last = 0

    def cache_update(self):
        if time.time() >= self.cache_last + self.cache_timeout:
            self.cache_last = time.time()
            self.text = self.http_parser(requests.get(self.http_url))
    
    def render(self, surface: Surface, clock: Clock):
        self.cache_update()
        super(HTTPTextDisplay, self).render(surface, clock)


class HTTPBoolDisplay(BoolDisplay):
    def __init__(
        self,
        prefix: str,
        url: str,
        parser: Callable[..., bool],
        cache_timeout: int = 300,
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
        """Displays a boolean from the given ``url``, parsed by the ``parser``
        callable before display.

        Results are cached for ``cache_timeout`` seconds.

        Other parameters are the same as ``rendash.plugins.basics.BoolDisplay``
        """

        super(HTTPBoolDisplay, self).__init__(
            None,
            prefix,
            font,
            text_true,
            text_false,
            text_none,
            color_bg_true,
            color_bg_false,
            color_bg_none,
            color_fg,
            multi_line,
            center,
            padding,
        )

        self.http_url = url
        self.http_parser = parser
        self.cache_timeout = cache_timeout
        self.cache_last = 0

    def cache_update(self):
        if time.time() >= self.cache_last + self.cache_timeout:
            self.cache_last = time.time()
            self.value = self.http_parser(requests.get(self.http_url))
    
    def render(self, surface: Surface, clock: Clock):
        self.cache_update()
        super(HTTPBoolDisplay, self).render(surface, clock)
