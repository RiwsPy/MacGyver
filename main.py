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
    window_id.refresh_window(map_id)
    dict_player_movement = \
        {K_RIGHT: "right", K_LEFT: "left", K_UP: "up", K_DOWN: "down"}

    while continue_main:
        pygame.time.Clock().tick(FPS_MAX)  # limitation to 30 loops/seconde
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue_main = False
                elif event.key in dict_player_movement:
                    if player.move(dict_player_movement[event.key]):
                        window_id.refresh_window(map_id)
            elif event.type == QUIT:
                continue_main = False

if __name__ == "__main__":
    main()
