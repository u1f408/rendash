from pygame.event import Event

class BasePlugin:
    def before_start(self):
        pass

    def after_stop(self):
        pass

    def on_event(self, event: Event):
        pass
