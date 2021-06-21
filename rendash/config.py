import types
import pygame
import paho.mqtt.client as mqtt

from pathlib import Path


class Config:
    def __init__(self):
        self.raw_values = {}
        self.mqtt_client = mqtt.Client()

    def __getitem__(self, *args):
        return self.raw_values.__getitem__(*args)

    def __setitem__(self, *args):
        return self.raw_values.__setitem__(*args)

    def load_from_file(self, path):
        d = types.ModuleType("config")
        d.__file__ = str(path)

        with open(path, 'rb') as fh:
            exec(compile(fh.read(), str(path), "exec"), d.__dict__)

        self.load_from_object(d)

    def load_from_object(self, obj):
        self.raw_values = dict(obj.__dict__)

    @property
    def mqtt_enabled(self):
        return self.raw_values.get('MQTT_SERVER', None) is not None

    @property
    def mqtt_server(self):
        return self.raw_values.get('MQTT_SERVER', ('127.0.0.1', 1883))

    def mqtt_connect(self):
        host, port = self.mqtt_server
        self.mqtt_client.connect_async(host, port=port)
        self.mqtt_client.loop_start()

    def mqtt_disconnect(self):
        self.mqtt_client.disconnect()

    @property
    def framerate(self):
        return self.raw_values.get('FRAMERATE', 30)

    @property
    def color_bg(self):
        return pygame.Color(self.raw_values.get('COLOR_BG', (0, 0, 0)))

    @property
    def color_fg(self):
        return pygame.Color(self.raw_values.get('COLOR_FG', (255, 255, 255)))

    @property
    def font(self):
        font_path = self.raw_values.get('FONT_FACE', 'DeJaVu Sans Mono')
        font_size = self.raw_values.get('FONT_SIZE', 16)

        if Path(font_path).is_file():
            return pygame.font.Font(font_path, font_size)
        else:
            return pygame.font.SysFont(font_path, font_size)

    def screen_flags(self):
        flags = pygame.RESIZABLE | pygame.DOUBLEBUF
        if self.raw_values.get('FULLSCREEN', False):
            flags |= pygame.FULLSCREEN

        return flags

    def root_object(self):
        root_object = self.raw_values.get('ROOT_OBJECT', None)
        if root_object is None:
            from rendash.plugins.basics import TextDisplay
            root_object = TextDisplay("No root object in config!")

        return root_object
    

current_config = Config()
