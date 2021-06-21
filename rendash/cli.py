from rendash import __version__
from rendash.main import main_loop
from rendash.config import current_config

from pathlib import Path

import argparse
import pygame


def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version=f"%(prog)s {__version__}")
    parser.add_argument('config', metavar='CONFIG', help='path to configuration file')
    return parser


def main():
    parser = argument_parser()
    args = parser.parse_args()

    # set up pygame
    pygame.init()

    # import config
    current_config.load_from_file(Path(args.config))

    # connect to MQTT
    if current_config.mqtt_enabled:
        current_config.mqtt_connect()

    # create screen and clock
    screen = pygame.display.set_mode((0, 0), current_config.screen_flags(), 32)
    clock = pygame.time.Clock()

    # run the before_start
    current_config.root_object().before_start()

    # run the main loop
    running = True
    while running:
        running = main_loop(screen, clock)

    # clean up!
    current_config.root_object().after_stop()
    current_config.mqtt_disconnect()
    pygame.quit()

    return 0
