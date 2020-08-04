#coding: utf-8

from classes.locale import IMAGE_WALL, IMAGE_GUARD, IMAGE_STAIR, IMAGE_GROUND, IMAGE_DEPARTURE, CASE_SIZE, WINDOW_SIZE
import pygame


class Game_window:
    def __init__(self) -> None:
        if WINDOW_SIZE < 1:
            print(f"WINDOW_SIZE error, must be superior than 0.")
            return None

        self.id = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE)) # initialisation de la fenêtre
        self.wall = pygame.image.load(IMAGE_WALL)
        self.guard = pygame.image.load(IMAGE_GUARD)
        self.stair = pygame.image.load(IMAGE_STAIR)
        self.ground = pygame.image.load(IMAGE_GROUND)
        self.departure = pygame.image.load(IMAGE_DEPARTURE)

    def refresh_window(self, map_id) -> None:
        #self.id.blit(self.background, (0, 0)) # collage de l'image de fond

        for height, line in enumerate(map_id.structure):
            for width, letter in enumerate(line):
                target = None
                if letter == 'W': # wall
                    target = self.wall
                elif letter == 'D': # departure
                    target = self.departure
                else: # ground
                    target = self.ground

                self.id.blit(target, (width * CASE_SIZE, height * CASE_SIZE))

                if letter == 'G': # guard
                    target = self.guard
                    self.id.blit(target, (width * CASE_SIZE, height * CASE_SIZE))
                elif letter == 'S': # stair
                    target = self.stair
                    self.id.blit(target, (width * CASE_SIZE, height * CASE_SIZE))

        # classes.map.refresh_map(self.items)
        for item in map_id.items:
            self.id.blit(item.image, (item.pos_x * CASE_SIZE, item.pos_y * CASE_SIZE))

        pygame.display.flip() # rafraîchissement de la fenêtre
        # possibilité de rafraîchir que les cases ayant changé d'état ?
