import pygame
from classes import map
from classes import window
from random import choice
from locale import *
import locale
from pygame.locals import *

class Entity:
    """doc string : help(Item)"""
    """séparer les class dans différents fichiers, dans un sous-dossier"""
    def __init__(self, icon, is_item = False):
        global MAP, WINDOW
        MAP = locale.MAP
        WINDOW = locale.WINDOW
        
        self.is_item = is_item
        self.image = pygame.image.load(icon).convert_alpha()

        if is_item:
            self.pos_x, self.pos_y = self.random_position()
        else:
            self.pos_x, self.pos_y = MAP.PJ_initial_position

        MAP.items.append(self)

    def move(self, direction):
        is_moving = False

        if direction == K_RIGHT:
            is_moving = self.check_move(1, 0)
        elif direction == K_LEFT:
            is_moving = self.check_move(-1, 0)
        elif direction == K_UP:
            is_moving = self.check_move(0, -1)
        elif direction == K_DOWN:
            is_moving = self.check_move(0, 1)

        if is_moving:
            for item in MAP.items: # collision
                if self != item and self.pos_x == item.pos_x and self.pos_y == item.pos_y: # no collision with himself
                    self.pick_up(item)

            if MAP.sprite(self.pos_x, self.pos_y) == 'G': # guard
                if self.state == 3: # 3 objets en sa possession
                    print("Vous endormissez le garde !")
                    self.state = 4
                elif self.state < 3:
                    print("Le garde vous vois ! C'est la mort !")
                    self.state = 9
            elif MAP.sprite(self.pos_x, self.pos_y) == 'S': # + vérif ou endormissement gardien
                print("Vous vous échappez du labyrinthe ! Fin de partie !")
                self.state = 8


    def check_move(self, x, y):
        """this function checks the new position of the player
        return False if :
            the game is over or PJ is dead
            or new position aren't in the MAP_SIZE
            or new position is a Wall
        else:
            new position is saved
            window is refreshed
        """
        next_x = self.pos_x + x
        next_y = self.pos_y + y
        
        if self.state > 7:
            return False
        elif next_x < 0 or next_y < 0:
            return False
        elif next_x >= MAP_SIZE or next_y >= MAP_SIZE:
            return False
        elif MAP.sprite(next_x, next_y) == 'W':
            return False

        self.pos_x = next_x
        self.pos_y = next_y
        WINDOW.blit()

        return True

    def pick_up(self, item):
        """if PJ and item position are the same
        item is removed from the ground
        self.state is incremented
        window is refreshed"""
        print("Great job! You found an object.")
        if self.state < 3: # problème si on augmente le nombre d'objets ?
            self.state += 1
        if self.state == 3:
            print("Vous fabriquez une serringue pour endormir le garde !")
        MAP.items.remove(item)
        WINDOW.blit()
        
    def random_position(self):
        """The position of the objets is random.
        Two objects can't have the same position.
        The location must be available."""
        # OU ??
        # nb = randrange(len(map.empty_case))
        # return map.empty_case.pop(nb)

        nb = choice(MAP.empty_case)
        MAP.empty_case.remove(nb)
        return nb