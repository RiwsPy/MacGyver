# coding: utf-8

import pygame
from classes import window, map, entity
from classes.locale import FPS_MAX
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RIGHT, K_LEFT, K_UP,\
    K_DOWN

"""
Labyrinthe game : MacGyver must escape !

Script Python
Files:
------
"""


"""les conseils d'Olivier :

* Faire un fichier "main" avec à l’intérieur un  if __name__ == '__main__'
* Séparer les classes en fichiers et les mettres dans un sous dossier
    et y ajouter un __init__.py
* Facultatif : Utiliser les types hints"""


def main() -> None:
    # game window initialisation
    window_id = window.Game_window()
    map_id = map.Map()

    if map_id.check_Map(window_id, map_id):
        game_loop(window_id, map_id)


def game_loop(window_id, map_id) -> None:
    continuer = True

    while continuer:
        pygame.time.Clock().tick(FPS_MAX)  # limitation à 30 boucles/seconde
        for event in pygame.event.get():
            if event.type == QUIT or \
                    event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer = False
            elif event.type == KEYDOWN and event.key in \
                    [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                player = entity.Entity.get_player_id()
                player.move(window_id, map_id, event.key)


if __name__ == "__main__":
    main()
