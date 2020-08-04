# coding: utf-8

import pygame
from random import choice
from classes.locale import MAP_SIZE, ITEM_NUMBER
from pygame.locals import K_RIGHT, K_LEFT, K_UP, K_DOWN


class Entity:
    """doc string : help(Item)"""
    def __init__(self, map_id, icon: str, is_item=True) -> None:
        """ generate all entities in the labyrinthe """
        self.map = map_id
        self.is_item = is_item
        self.image = pygame.image.load(icon).convert_alpha()
        self.state = 0

        if is_item:
            self.pos_x, self.pos_y = self.random_position()
        else:
            global PLAYER
            PLAYER = self
            self.pos_x, self.pos_y = map_id.PJ_initial_position

        map_id.items.append(self)

    @staticmethod
    def get_player_id():
        return PLAYER

    def move(self, window_id, map_id, direction: int) -> None:
        move_x, move_y = 0, 0

        if direction == K_RIGHT:
            move_x, move_y = 1, 0
        elif direction == K_LEFT:
            move_x, move_y = -1, 0
        elif direction == K_UP:
            move_x, move_y = 0, -1
        elif direction == K_DOWN:
            move_x, move_y = 0, 1

        if self.check_move(window_id, map_id, move_x, move_y):
            for item in self.map.items:  # collision
                if self != item and self.pos_x == item.pos_x and\
                        self.pos_y == item.pos_y:  # no collision with himself
                    self.pick_up(window_id, map_id, item)

            if self.map.my_sprite(self) == 'G':  # guard
                if self.state == ITEM_NUMBER:
                    print("Vous endormissez le garde !")
                    self.state += 1
                elif self.state < ITEM_NUMBER:
                    print("Le garde vous vois ! C'est la mort !")
                    self.state = 9
            elif self.map.my_sprite(self) == 'S':
                print("Vous vous échappez du labyrinthe ! Fin de partie !")
                self.state = 8

    def check_move(self, window_id, map_id, x: int, y: int) -> bool:
        """this function checks the new position of the player
        return False if :
            the move is (0, 0) (no move)
            the game is over or PJ is dead
            or new position aren't in the MAP_SIZE
            or new position is a Wall
        else:
            new position is saved
            window is refreshed
        """
        if x == 0 and y == 0:
            return False

        next_x = self.pos_x + x
        next_y = self.pos_y + y

        if self.state > 7:
            return False
        elif next_x < 0 or next_y < 0:
            return False
        elif next_x >= MAP_SIZE or next_y >= MAP_SIZE:
            return False
        elif self.map.sprite(next_x, next_y) == 'W':
            return False

        self.pos_x = next_x
        self.pos_y = next_y
        window_id.refresh_window(map_id)

        return True

    def pick_up(self, window_id, map_id, item) -> None:
        """if PJ and item position are the same
        item is removed from the ground
        self.state is incremented
        window is refreshed"""
        print("Great job! You found an object.")
        if self.state < ITEM_NUMBER:
            self.state += 1
        if self.state == ITEM_NUMBER:
            print("Vous fabriquez une serringue pour endormir le garde !")
        self.map.items.remove(item)
        window_id.refresh_window(map_id)

    def random_position(self) -> tuple:
        """The position of the objets is random.
        Two objects can't have the same position.
        The location must be available."""
        # OU ??
        # nb = randrange(len(map.empty_case))
        # return map.empty_case.pop(nb)

        nb = choice(self.map.empty_case)
        self.map.empty_case.remove(nb)
        return nb
