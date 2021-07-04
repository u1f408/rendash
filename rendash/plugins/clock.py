from typing import Union

from rendash.plugins import BasePlugin
from rendash.config import current_config
from rendash.utils.text import draw_text

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

import pygame
from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock
from pygame.event import Event


class ClockDisplay(BasePlugin):
    def __init__(
        self,
        text: str,
        tz: str,
        font_time: Font = None,
        font_desc: Font = None,
        color_bg: Color = None,
        color_fg: Color = None,
        padding: int = 8,
    ):
        """Display the time in a given IANA timezone.
    
        If any of the `font`, `color_bg`, or `color_fg` parameters are None,
        the values from ``current_config`` are used.
        """

        self.text = text
        self.tz = ZoneInfo(tz)
        self.font_time = font_time
        self.font_desc = font_desc
        self.color_bg = color_bg
        self.color_fg = color_fg
        self.padding = padding

    def __repr__(self):
        return f"<{self.__class__.__name__} tz={repr(self.tz)}>"
    
    def before_start(self):
        self.font_time = self.font_time or current_config.font
        self.font_desc = self.font_desc or current_config.font
        self.color_bg = self.color_bg or current_config.color_bg
        self.color_fg = self.color_fg or current_config.color_fg

    def render(self, surface: Surface, clock: Clock):
        surface.fill(self.color_bg)

        # Draw the description text
        desc_surface = Surface((
            surface.get_width() - (self.padding * 2),
            int((surface.get_height() / 4) * 1) - self.padding,
        ))

        desc_surface.fill(self.color_bg)
        draw_text(str(self.text), desc_surface, desc_surface.get_rect(), self.font_desc, self.color_fg, center=True)

        desc_draw_rect = Rect(
            self.padding,
            #int((surface.get_height() / 4) * 2) + self.padding,
            self.padding,
            desc_surface.get_width(),
            desc_surface.get_height(),
        )

        surface.blit(desc_surface, desc_draw_rect)

        # Draw the time
        current_time = datetime.now(tz=self.tz)
        clock_text = [
            current_time.strftime("%Y-%m-%d"),
            current_time.strftime("%H:%M"),
        ]

        clock_surface = Surface((
            surface.get_width() - (self.padding * 2),
            int((surface.get_height() / 4) * 2) - self.padding,
        ))

        clock_surface.fill(self.color_bg)
        draw_text(clock_text, clock_surface, clock_surface.get_rect(), self.font_time, self.color_fg, center=True)

        clock_draw_rect = Rect(
            self.padding,
            int((surface.get_height() / 4) * 1) + self.padding,
            clock_surface.get_width(),
            clock_surface.get_height(),
        )

        surface.blit(clock_surface, clock_draw_rect)

        # Draw the timezone
        tz_surface = Surface((
            surface.get_width() - (self.padding * 2),
            int((surface.get_height() / 3) * 1) - self.padding,
        ))

        tz_surface.fill(self.color_bg)
        draw_text(str(self.tz), tz_surface, tz_surface.get_rect(), self.font_desc, self.color_fg, center=True)

        tz_draw_rect = Rect(
            self.padding,
            int((surface.get_height() / 4) * 3) + self.padding,
            tz_surface.get_width(),
            tz_surface.get_height(),
        )

        surface.blit(tz_surface, tz_draw_rect)
