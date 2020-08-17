# coding: utf-8

"""
    Class to manage the window
"""

from classes.locale import IMAGE_GROUND, CASE_SIZE, WINDOW_SIZE,\
    WINDOW_TITLE, IMAGE_WALL, MAP_SIZE
import pygame


class WindowManager:
    """
        Initializes the game window
    """
    def __init__(self) -> None:
        """
            Window initialisation
        """
        if WINDOW_SIZE < 2:
            print("WINDOW_SIZE error, must be superior than 1.")
            return None

        # window's initialisation
        self.id = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.wall_icon = pygame.image.load(IMAGE_WALL)
        self.ground_icon = pygame.image.load(IMAGE_GROUND)

        # window's title
        pygame.display.set_caption(WINDOW_TITLE)

    def refresh_window(self, map_id) -> None:
        """
            Refresh the game window

            *param map_id: of the map to refresh
            *type map_id: map.MapManager
            *return: None
        """
        for y in range(MAP_SIZE):
            for x in range(MAP_SIZE):
                position = (x * CASE_SIZE, y * CASE_SIZE)

                if map_id.is_valid_position((x, y)):
                    self.id.blit(self.ground_icon, position)
                    if (x, y) in map_id.entity_position:
                        self.id.blit(map_id.entity_position[(x, y)].icon,
                                     position)
                else:
                    self.id.blit(self.wall_icon, position)

        pygame.display.flip()  # window refresh
