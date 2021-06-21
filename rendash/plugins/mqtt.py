from rendash.config import current_config
from rendash.plugins.basics import TextDisplay, BoolDisplay

from pygame import Surface, Rect, Color
from pygame.font import Font
from pygame.time import Clock


class MQTTTextDisplay(TextDisplay):
    def __init__(
        self,
        topic: str,
        font: Font = None,
        color_bg: Color = None,
        color_fg: Color = None,
        center: bool = True,
        padding: int = 8,
    ):
        """Displays text from the MQTT topic `topic`.

        Other parameters are the same as ``rendash.plugins.basics.TextDisplay``
        """

        super(MQTTTextDisplay, self).__init__(
            f"Waiting for MQTT (topic {repr(topic)})",
            font,
            color_bg,
            color_fg,
            center,
            padding,
        )

        self.topic = topic

    def before_start(self):
        current_config.mqtt_client.message_callback_add(self.topic, self.mqtt_callback)
        current_config.mqtt_client.subscribe(self.topic)

    def mqtt_callback(self, mqtt_client, mqtt_userdata, mqtt_message):
        if mqtt_message.topic == self.topic:
            self.text = mqtt_message.payload


class MQTTBoolDisplay(BoolDisplay):
    def __init__(
        self,
        topic: str,
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
        """Displays a boolean from the MQTT topic `topic`.

        Message contents ``0``, ``false``, and ``no`` (case insensitive) are
        treated as False, and ``1``, ``true``, and ``yes`` (case insensitive)
        are treated as True. All other messages are set the value to None.

        Other parameters are the same as ``rendash.plugins.basics.BoolDisplay``
        """

        super(MQTTBoolDisplay, self).__init__(
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

        self.topic = topic

    def before_start(self):
        current_config.mqtt_client.message_callback_add(self.topic, self.mqtt_callback)
        current_config.mqtt_client.subscribe(self.topic)

    def mqtt_callback(self, mqtt_client, mqtt_userdata, mqtt_message):
        if mqtt_message.topic == self.topic:
            payload = mqtt_message.payload.lower()

            if payload == b'0' or payload == b'false' or payload == b'no':
                self.value = False
            elif payload == b'1' or payload == b'true' or payload == b'yes':
                self.value = True
            else:
                self.value = None
