from typing import Any

from rendash.config import current_config
from rendash.plugins import BasePlugin
from rendash.plugins.basics import TextDisplay, Button
from rendash.plugins.splits import VerticalSplit, HorizontalSplit

import pygame
from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock
from pygame.event import Event


class BubbleBase(BasePlugin):
    def __init__(self):
        self.inner = TextDisplay('')

    def render(self, surface: Surface, clock: Clock):
        self.inner.render(surface, clock)
    
    def on_event(self, event: Event):
        self.inner.on_event(event)
    
    def before_start(self):
        self.inner.before_start()

    def after_stop(self):
        self.inner.after_stop()


class PageNavigation(BubbleBase):
    def __init__(self, paginator):
        self.paginator = paginator
        self.inner = HorizontalSplit([
            (20, TextDisplay("this is a bug", center=False)),
            (1, Button("<", on_click=lambda _: self.page_prev(), center=True)),
            (1, Button(">", on_click=lambda _: self.page_next(), center=True)),
        ])

    def __repr__(self):
        return f"<{self.__class__.__name__} paginator={repr(self.paginator)} inner={repr(self.inner)}>"

    def before_start(self):
        super(PageNavigation, self).before_start()
        self.page_update()

    def page_update(self):
        current = self.paginator.current_page + 1
        total = len(self.paginator.pages)
        self.inner.portions[0][1].text = f"Page {current} of {total}"

    def page_prev(self):
        self.paginator.page_prev()
        self.page_update()

    def page_next(self):
        self.paginator.page_next()
        self.page_update()


class Paginator(BubbleBase):
    def __init__(self, pages, size: tuple = (1, 10)):
        self.size = size
        self.current_page = 0
        self.pages = pages
        self.inner = VerticalSplit([
            (self.size[0], PageNavigation(self)),
        ])

    def __repr__(self):
        return f"<{self.__class__.__name__} current_page={repr(self.current_page)} pages={repr(self.pages)}>"
    
    def page_update(self):
        while len(self.inner.portions) > 1:
            self.inner.portions.pop()

        self.inner.portions.append((self.size[1], self.pages[self.current_page]))

    def page_prev(self):
        self.current_page -= 1
        if self.current_page < 0:
            self.current_page = len(self.pages) - 1

        self.page_update()

    def page_next(self):
        self.current_page += 1
        if self.current_page >= len(self.pages):
            self.current_page = 0

        self.page_update()

    def before_start(self):
        self.page_update()
        super(Paginator, self).before_start()

        for page in self.pages:
            page.before_start()

    def after_stop(self):
        while len(self.inner.portions) > 1:
            self.inner.portions.pop()

        super(Paginator, self).after_stop()
        for page in self.pages:
            page.after_stop()

