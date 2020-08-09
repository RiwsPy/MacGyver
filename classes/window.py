# coding: utf-8

from classes.locale import IMAGE_GUARD, IMAGE_STAIR, IMAGE_GROUND,\
    IMAGE_DEPARTURE, CASE_SIZE, WINDOW_SIZE, WINDOW_TITLE, IMAGE_WALL
import pygame


class Game_window:
    """
        Initializes the game window
    """
    def __init__(self) -> None:
        if WINDOW_SIZE < 1:
            print("WINDOW_SIZE error, must be superior than 0.")
            return None

        # window initialisation
        self.id = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.wall = pygame.image.load(IMAGE_WALL)
        self.departure = pygame.image.load(IMAGE_DEPARTURE)
        self.ground = pygame.image.load(IMAGE_GROUND)
        self.guard = pygame.image.load(IMAGE_GUARD)
        self.stair = pygame.image.load(IMAGE_STAIR)

        pygame.display.set_caption(WINDOW_TITLE)

    def refresh_window(self, map_id) -> None:
        """
            Refresh the game window

            *param map_id: of the map to refresh
            *type map_id: map.Map
            *return: None
        """
        for pos_y, line in enumerate(map_id.structure):
            for pos_x, letter in enumerate(line):
                target = None
                if letter == 'W':  # wall
                    target = self.wall
                elif letter == 'D':  # departure
                    target = self.departure
                else:  # ground
                    target = self.ground

                position = (pos_x * CASE_SIZE, pos_y * CASE_SIZE)
                self.id.blit(target, position)

                if letter == 'G':  # guard
                    self.id.blit(self.guard, position)
                elif letter == 'S':  # stair
                    self.id.blit(self.stair, position)

        for item in map_id.items:
            self.id.blit(
                item.image, (item.pos_x * CASE_SIZE, item.pos_y * CASE_SIZE))

        pygame.display.flip()  # window refresh
