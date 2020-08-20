# coding: utf-8

import pygame
from game import window, map
from config.locale import MAP_FILENAME, FPS_MAX
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE,\
    K_RIGHT, K_LEFT, K_UP, K_DOWN


def main() -> None:
    """
        Run the game
        *return: None
    """
    # game window initialisation
    map_id = map.MapManager()
    window_id = window.WindowManager()

    player = map_id.load_from_file(MAP_FILENAME)
    if player:
        main_loop(player, window_id, map_id)


def main_loop(player, window_id, map_id) -> None:
    """
        Waiting for an event
        *param player: id of player
        *param window_id: id of window
        *param map_id: id of map
        *type player: entity.EntityManager
        *type window_id: window.WindowManager
        *type map_id: map.MapManager
        *return: None
    """
    continue_main = True
    event_to_method = \
        {K_RIGHT: "right", K_LEFT: "left", K_UP: "up", K_DOWN: "down"}

    window_id.refresh_all(map_id)
    while continue_main:
        pygame.time.Clock().tick(FPS_MAX)  # limitation to 30 loops/seconde
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue_main = False
                elif event.key in event_to_method:
                    positions_refresh = player.move(event_to_method[event.key])
                    window_id.refresh_soft(map_id, positions_refresh)
            elif event.type == QUIT:
                continue_main = False


if __name__ == "__main__":
    main()
