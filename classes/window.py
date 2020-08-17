# coding: utf-8

"""
    Class to manage the window
"""

from classes.locale import IMAGE_GUARD, IMAGE_STAIR, IMAGE_GROUND,\
    IMAGE_DEPARTURE, CASE_SIZE, WINDOW_SIZE, WINDOW_TITLE, IMAGE_WALL, MAP_SIZE
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
        self.departure_icon = pygame.image.load(IMAGE_DEPARTURE)
        self.ground_icon = pygame.image.load(IMAGE_GROUND)
        self.guard_icon = pygame.image.load(IMAGE_GUARD)
        self.stair_icon = pygame.image.load(IMAGE_STAIR)

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

                    if (x, y) == map_id.guard_position:
                        self.id.blit(self.guard_icon, position)
                    elif (x, y) == map_id.stair_position:
                        self.id.blit(self.stair_icon, position)
                    elif (x, y) == map_id.start_position:
                        self.id.blit(self.departure_icon, position)
                else:
                    self.id.blit(self.wall_icon, position)

        for item in map_id.items:
            self.id.blit(
                item.icon, (item.pos_x * CASE_SIZE, item.pos_y * CASE_SIZE))

        pygame.display.flip()  # window refresh
