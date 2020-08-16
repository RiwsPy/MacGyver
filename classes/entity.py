# coding: utf-8

"""
    Items and player of the game
"""

import pygame
from classes.locale import ITEMS_NUMBER, STATE_DEAD, STATE_OVER,\
    GUARD_CHAR, STAIR_CHAR
from pygame.locals import K_RIGHT, K_LEFT, K_UP, K_DOWN


class EntityManager:
    """
        Generate an entity in the labyrinth
    """
    def __init__(self, map_id, icon: str, position: tuple) -> None:
        """
            *param map_id: map id
            *param icon: icon file name
            *param position: entity's position
            *type map_id: map.MapManager
            *type icon: str
            *type position: tuple
            *return: None
        """

        self.map = map_id
        self.image = pygame.image.load(icon).convert_alpha()
        self._position = position
        self.state = 0

    @property
    def pos_x(self) -> int:
        """
            *return: x-axis of the entity
            *rtype: int
        """
        return self.position[0]

    @property
    def pos_y(self) -> int:
        """
            *return: y-axis of the entity
            *rtype: int
        """
        return self.position[1]

    @property
    def position(self) -> tuple:
        """
            *return: (x-axis, y-axis) of the entity
            *rtype: tuple
        """
        return self._position

    @position.setter
    def position(self, value: tuple) -> None:
        """
            Erase the entity's position by an another
            *param value: tuple of the new position
            *type value: tuple
            *return: None
        """
        if type(value) == tuple:
            self._position = value

    def game_loop_entity(self, event) -> bool:
        """
            Wait a keyboard event
            *param event: keyboard event
            *type event: pygame.event
            *return: True if the key is managed, False otherwise
            *rtype: bool
        """
        if event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
            self.move(event.key)
            return True
        return False

    def move(self, direction: int) -> None:
        """
            Allows the entity to move in the map

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
            self.position = (self.pos_x + move_x, self.pos_y + move_y)
            for item in self.map.items:  # collision
                # no collision with himself
                if self != item and self.position == item.position:
                    self.pick_up(item)

            letter = self.map.my_sprite(self)
            if letter == GUARD_CHAR:  # guard
                self.meet_guard()
            elif letter == STAIR_CHAR:  # stair
                self.end_game()

    def check_move(self, x: int, y: int) -> bool:
        """
            Check if the new position of the entity is available

            *param x: x-axis movement
            *param y: y-axis movement
            *type x: int
            *type y: int
            *return: True if the entity can move, False otherwise
            *rtype: bool
        """
        if x == 0 and y == 0:
            return False
        elif self.state == STATE_OVER or \
                self.state == STATE_DEAD:
            return False

        next_x = self.pos_x + x
        next_y = self.pos_y + y

        return self.map.is_valid_position((next_x, next_y))

    def pick_up(self, item) -> None:
        """
            If PJ and item position are the same:
            * item is removed from the ground
            * self.state is incremented

            *param item: item id
            *type item: entity.EntityManager
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
