# coding: utf-8

import pygame
from classes import window, map
from classes.locale import FPS_MAX, MAP_FILENAME
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE


def main() -> None:
    """
        Run the game
    """
    # game window initialisation
    map_id = map.MapManager()
    window_id = window.WindowManager()

    player = map_id.load_from_file(MAP_FILENAME)
    if player:
        game_loop(player, window_id, map_id)


def game_loop(player, window_id, map_id) -> None:
    """
        Main loop
        Waiting for an event
    """
    continue_main = True
    window_id.refresh_window(map_id)

    while continue_main:
        pygame.time.Clock().tick(FPS_MAX)  # limitation to 30 loops/seconde
        for event in pygame.event.get():
            if event.type == QUIT or \
                    event.type == KEYDOWN and event.key == K_ESCAPE:
                continue_main = False
            elif event.type == KEYDOWN:
                if player.game_loop_entity(event):
                    window_id.refresh_window(map_id)


if __name__ == "__main__":
    main()
