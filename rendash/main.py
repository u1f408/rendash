from rendash.config import current_config

import pygame


def main_loop(screen, clock):
    # get our root object
    root_object = current_config.root_object()

    # fill the background
    screen.fill(current_config.color_bg)

    # render our root object
    root_object.render(screen, clock)
    
    # dispatch events
    for event in pygame.event.get():
        # allow quitting
        if event.type == pygame.QUIT:
            return False

        elif event.type == pygame.KEYDOWN:
            # exit the dashboard on pressing Q
            if event.key == pygame.K_q:
                return False

        root_object.on_event(event)

    # flip the display
    pygame.display.flip()
    clock.tick(current_config.framerate)

    return True
