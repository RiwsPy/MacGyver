# coding: utf-8

"""
    Class to manage the window
"""

from config.locale import IMAGE_GROUND, CASE_SIZE, WINDOW_SIZE,\
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

    def refresh_all(self, map_id) -> None:
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
                else:
                    self.id.blit(self.wall_icon, position)

        for position, id in map_id.entity_position.items():
            position = (position[0] * CASE_SIZE, position[1] * CASE_SIZE)
            self.id.blit(id.icon, position)

        pygame.display.flip()  # window refresh

    def refresh_soft(self, map_id, positions: tuple) -> None:
        """
            Refresh specific position in game window

            *param map_id: of the map to refresh
            *param positions: tuple of two positions to refresh
            *type map_id: map.MapManager
            *type positions: tuple(tuple, tuple)
            *return: None
        """
        for position in positions:
            pixel_position = (position[0]*CASE_SIZE, position[1]*CASE_SIZE)
            self.id.blit(self.ground_icon, pixel_position)
            if position in map_id.entity_position:
                self.id.blit(map_id.entity_position[position].icon,
                             pixel_position)

        pygame.display.flip()  # window refresh
