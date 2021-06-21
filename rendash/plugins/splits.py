from typing import Any

from rendash.config import current_config
from rendash.plugins import BasePlugin

import pygame
from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock
from pygame.event import Event

class Splitter(BasePlugin):
    def __init__(self, portions, padding: int = 8):
        self.padding = 8
        self.portions = []
        for portion in portions:
            if not isinstance(portion, tuple):
                portion = (1, portion,)
            self.portions.append(portion)

    def _split(self, screen_size: int) -> list[tuple[int, Any]]:
        portions = []

        total_size = sum(map(lambda x: x[0], self.portions))
        single_size = (screen_size // total_size)

        for (size, portion) in self.portions:
            size = (single_size * size) - (self.padding * 2)
            portions.append((size, portion))
            
        return portions

    def before_start(self):
        for (_, portion) in self.portions:
            portion.before_start()

    def after_stop(self):
        for (_, portion) in self.portions:
            portion.after_stop()


class HorizontalSplit(Splitter):
    def render(self, surface: Surface, clock: Clock):
        surface.fill(current_config.color_bg)

        self._last_surface_width = surface.get_width()
        self._last_surface_height = surface.get_height()
        portions = self._split(self._last_surface_width)
        
        x = self.padding
        for (size, portion) in portions:
            # get the rect containing this portion, and a surface to contain it
            rect = Rect(x, self.padding, size, self._last_surface_height - (self.padding * 2))
            portion_surface = Surface((rect.width, rect.height))

            # render the portion
            portion.render(portion_surface, clock)

            # and blit that to the screen
            surface.blit(portion_surface, rect)
            x += size + (self.padding * 2)

    def on_event(self, event: Event):
        portion_rects = []
        portions = self._split(self._last_surface_width)

        x = self.padding
        for (size, portion) in portions:
            # get the rect containing this portion
            rect = Rect(x, self.padding, size, self._last_surface_height - (self.padding * 2))
            x += size + (self.padding * 2)
            portion_rects.append((portion, rect))

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            for (portion, rect) in portion_rects:
                if rect.collidepoint(event.pos):
                    event.pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                    portion.on_event(event)

class VerticalSplit(Splitter):
    def render(self, surface: Surface, clock: Clock):
        surface.fill(current_config.color_bg)

        self._last_surface_width = surface.get_width()
        self._last_surface_height = surface.get_height()
        portions = self._split(self._last_surface_height)
        
        y = self.padding
        for (size, portion) in portions:
            # get the rect containing this portion, and a surface to contain it
            rect = Rect(self.padding, y, self._last_surface_width - (self.padding * 2), size)
            portion_surface = Surface((rect.width, rect.height))

            # render the portion
            portion.render(portion_surface, clock)

            # and blit that to the screen
            surface.blit(portion_surface, rect)
            y += size + (self.padding * 2)

    def on_event(self, event: Event):
        portion_rects = []
        portions = self._split(self._last_surface_height)
        
        y = self.padding
        for (size, portion) in portions:
            # get the rect containing this portion, and a surface to contain it
            rect = Rect(self.padding, y, self._last_surface_width - (self.padding * 2), size)
            y += size + (self.padding * 2)
            portion_rects.append((portion, rect))

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            for (portion, rect) in portion_rects:
                if rect.collidepoint(event.pos):
                    event.pos = (event.pos[0] - rect.left, event.pos[1] - rect.top)
                    portion.on_event(event)
