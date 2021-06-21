from rendash.config import current_config
from rendash.plugins.basics import TextDisplay, BoolDisplay, Button
from rendash.plugins.page import Paginator

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
        super(MQTTTextDisplay, self).before_start()
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
        super(MQTTBoolDisplay, self).before_start()
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

class MQTTButton(Button):
    def __init__(
        self,
        mqtt_topic: str,
        mqtt_message: str,
        text: str = "Tap to alert",
        font: Font = None,
        color_bg: Color = None,
        color_fg: Color = None,
        center: bool = True,
        padding: int = 8,
    ):
        """Button that pushes a defined message to an MQTT topic when clicked.

        ``mqtt_topic`` is the topic to push to, ``mqtt_message`` is the message to push.

        Other parameters are the same as ``rendash.plugins.basics.Button``
        """

        super(MQTTButton, self).__init__(
            text,
            self.on_click,
            font,
            color_bg,
            color_fg,
            center,
            padding,
        )

        self.mqtt_topic = mqtt_topic
        self.mqtt_message = mqtt_message

    def before_start(self):
        super(MQTTButton, self).before_start()
        current_config.mqtt_client.message_callback_add(self.mqtt_topic, self.mqtt_callback)
        current_config.mqtt_client.subscribe(self.mqtt_topic)

    def mqtt_callback(self, mqtt_client, mqtt_userdata, mqtt_message):
        if mqtt_message.topic == self.mqtt_topic:
            # do something?
            pass

    def on_click(self, event):
        current_config.mqtt_client.publish(self.mqtt_topic, self.mqtt_message)

class MQTTPaginator(Paginator):
    def __init__(
        self,
        mqtt_topic: str,
        pages,
        size: tuple = (1, 10),
    ):
        """A pagination widget where the selected page is determined by the
        value of an MQTT topic.

        ``mqtt_topic`` is the name of the topic to use for page selection.

        All other parameters are the same as ``rendash.plugins.page.Paginator``.
        """

        super(MQTTPaginator, self).__init__(
            pages,
            size, 
            show_pagination=False,
        )

        self.mqtt_topic = mqtt_topic

    def __repr__(self):
        return f"<{self.__class__.__name__} mqtt_topic={repr(self.mqtt_topic)} current_page={repr(self.current_page)} pages={len(self.pages)}>"

    def before_start(self):
        super(MQTTPaginator, self).before_start()
        current_config.mqtt_client.message_callback_add(self.mqtt_topic, self.mqtt_callback)
        current_config.mqtt_client.subscribe(self.mqtt_topic)

    def mqtt_callback(self, mqtt_client, mqtt_userdata, mqtt_message):
        if mqtt_message.topic == self.mqtt_topic:
            self.current_page = int(mqtt_message.payload) % len(self.pages)
            self.page_update()

