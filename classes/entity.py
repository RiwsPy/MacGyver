# coding: utf-8

import pygame
from random import choice
from classes.locale import MAP_SIZE, ITEMS_NUMBER, STATE_DEAD, STATE_OVER
from pygame.locals import K_RIGHT, K_LEFT, K_UP, K_DOWN


class Entity:
    """
        Generate an entity in the labyrinthe
    """
    def __init__(self, window_id, map_id, icon: str, is_item=True) -> None:
        """
            *param window_id: window id
            *param map_id: map id
            *param icon: icon file name
            *param is_item: true if the entity is an item
                false if is the player
            *type window_id: window.Game_window
            *type map_id: map.Map
            *type icon: str
            *is_item: bool
            *return: None
        """

        self.window = window_id
        self.map = map_id
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
        """
            *return: player's ID
            *rtype: entity.Entity
        """
        return PLAYER

    def move(self, direction: int) -> None:
        """
            Allows the entity to move in the map
            and refresh the window

            *param direction: pygame.event.key
            *type direction: int
            *return: None
        """
        move_x, move_y = 0, 0

        if direction == K_RIGHT:
            move_x = 1
        elif direction == K_LEFT:
            move_x = -1
        elif direction == K_UP:
            move_y = -1
        elif direction == K_DOWN:
            move_y = 1

        if self.check_move(move_x, move_y):
            for item in self.map.items:  # collision
                if self != item and self.pos_x == item.pos_x and\
                        self.pos_y == item.pos_y:  # no collision with himself
                    self.pick_up(item)

            letter = self.map.my_sprite(self)
            if letter == 'G':  # guard
                self.meet_guard()
            elif letter == 'S':  # stair
                self.end_game()

            self.window.refresh_window(self.map)

    def check_move(self, x: int, y: int) -> bool:
        """
            Check the new position of the entity
            return False if :
                * the move is (0, 0) (no move)
                * the game is over or PJ is dead
                * new position aren't in the MAP_SIZE
                * new position is a Wall
            else:
                * new position is saved

            *param x: x-axis movement
            *param y: y-axis movement
            *type x: int
            *type y: int
            *return: True if the entity can move, False otherwise
            *rtype: bool
        """
        if x == 0 and y == 0:
            return False

        next_x = self.pos_x + x
        next_y = self.pos_y + y

        if self.state == STATE_OVER or \
                self.state == STATE_DEAD:
            return False
        elif next_x < 0 or next_y < 0:
            return False
        elif next_x >= MAP_SIZE or next_y >= MAP_SIZE:
            return False
        elif self.map.sprite(next_x, next_y) == 'W':
            return False

        self.pos_x = next_x
        self.pos_y = next_y

        return True

    def pick_up(self, item) -> None:
        """
            If PJ and item position are the same:
            * item is removed from the ground
            * self.state is incremented

            *param item: item id
            *type item: entity.Entity
            *return: None
        """
        print("Great job! You found an object.")
        if self.state < ITEMS_NUMBER:
            self.state += 1
        if self.state == ITEMS_NUMBER:
            print("You craft a syringe to put the guard to sleep!")
        self.map.items.remove(item)

    def meet_guard(self) -> None:
        """
            The player meet the guard: what's going on ?

            *return: None
        """
        if self.state == ITEMS_NUMBER:
            print("You put the guard to sleep!")
            self.state += 1
        elif self.state < ITEMS_NUMBER:
            print("The guard sees you! It's death !")
            self.state = STATE_DEAD

    def end_game(self) -> None:
        """
            The game is ending

            *return: None
        """
        print("Congratulations! You escape from the labyrinth!\
            Game over !")
        self.state = STATE_OVER

    def random_position(self) -> tuple:
        """
            Object's position is randomly chosen
            Two objects can't have the same position
            The location must be available

            *return: (x-axis, y-axis)
            *rtype: tuple
        """
        nb = choice(self.map.empty_case)
        self.map.empty_case.remove(nb)
        return nb
