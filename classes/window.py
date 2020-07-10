#coding: utf-8

from locale import *
import locale
import pygame
from pygame.locals import *


def game_loop():
    continuer = True

    while continuer:
        pygame.time.Clock().tick(30) # limitation à 30 boucles/seconde
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer = False
            elif event.type == KEYDOWN and event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                locale.PLAYER.move(event.key)

    #os.system("pause")

class Game_window:
    def __init__(self) -> None:
        if WINDOW_SIZE < 1:
            print(f"WINDOW_SIZE error, must be superior than 0.")
            return None

        locale.WINDOW = self

        self.id = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE)) # initialisation de la fenêtre
        self.background = pygame.image.load(IMAGE_BACKGROUND).convert() # chargement de l'image + conversion dans les dimensions adéquates
        self.wall = pygame.image.load(IMAGE_WALL)
        self.guard = pygame.image.load(IMAGE_GUARD)
        self.stair = pygame.image.load(IMAGE_STAIR)
        self.departure = pygame.image.load(IMAGE_DEPARTURE)

    def refresh(self) -> None:
        self.id.blit(self.background, (0, 0)) # collage de l'image de fond

        for height, line in enumerate(locale.MAP.structure):
            for width, letter in enumerate(line):
                target = None
                if letter == 'W': # wall
                    target = self.wall
                elif letter == 'G': # guard
                    target = self.guard
                elif letter == 'S': # stair
                    target = self.stair
                elif letter == 'D': # departure
                    target = self.departure

                if target:
                    self.id.blit(target, (width * CASE_SIZE, height * CASE_SIZE))

        for item in locale.MAP.items:
            self.id.blit(item.image, (item.pos_x * CASE_SIZE, item.pos_y * CASE_SIZE))

        pygame.display.flip() # rafraîchissement de la fenêtre
        # possibilité de rafraîchir que les cases ayant changé d'état ?
