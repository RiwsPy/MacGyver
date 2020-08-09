# coding: utf-8

import pygame
from classes import window, map, entity
from classes.locale import FPS_MAX
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT, K_UP,\
    K_DOWN


def main() -> None:
    # game window initialisation
    window_id = window.Game_window()
    map_id = map.Map()

    if map_id.check_Map(window_id):
        game_loop()


def game_loop() -> None:
    run = True
    player = entity.Entity.get_player_id()

    while run:
        pygame.time.Clock().tick(FPS_MAX)  # limitation to 30 loops/seconde
        for event in pygame.event.get():
            if event.type == QUIT or \
                    event.type == KEYDOWN and event.key == K_ESCAPE:
                run = False
            elif event.type == KEYDOWN and event.key in \
                    [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                player.move(event.key)


if __name__ == "__main__":
    main()
