# coding: utf-8

"""
    Items and player of the game
"""

import pygame
from classes.locale import ITEMS_NUMBER, STATE_DEAD, STATE_OVER,\
    GUARD_CHAR, STAIR_CHAR


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
        self.icon = pygame.image.load(icon).convert_alpha()
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

    @property
    def right(self):
        """
            Move to right
        """
        return (self.pos_x + 1, self.pos_y)

    @property
    def left(self):
        """
            Move to left
        """
        return (self.pos_x - 1, self.pos_y)

    @property
    def up(self):
        """
            Move to up
        """
        return (self.pos_x, self.pos_y - 1)

    @property
    def down(self):
        """
            Move to down
        """
        return (self.pos_x, self.pos_y + 1)

    def move(self, event: str) -> None:
        """
            Allows the entity to move in the map

            *param event: method to apply
            *type event: str
            *return: None
        """
        next_position = getattr(self, event, self.position)
        if self.check_move(next_position):
            self.position = next_position
            for item in self.map.items:  # collision
                # no collision with himself
                if self != item and self.position == item.position:
                    self.pick_up(item)

            letter = self.map.sprite(self.position)
            if letter == GUARD_CHAR:  # guard
                self.meet_guard()
            elif letter == STAIR_CHAR:  # stair
                self.end_game()
            return True
        return False

    def check_move(self, position: tuple) -> bool:
        """
            Check if the new position of the entity is available

            *param position: (x-axis, y-axis) position
            *type position: tuple
            *return: True if the entity can move, False otherwise
            *rtype: bool
        """
        if self.position == position:
            return False
        elif self.state == STATE_OVER or \
                self.state == STATE_DEAD:
            return False

        return self.map.is_valid_position(position)

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
