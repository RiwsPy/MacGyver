# coding: utf-8

"""
    Items and player of the game
"""

import pygame
from config.locale import ITEMS_NUMBER, STATE_DEAD, STATE_OVER,\
    GUARD_CHAR, STAIR_CHAR, PATH_CHAR


class EntityManager:
    """
        Generate an entity in the labyrinth
    """
    def __init__(self, map_id, icon: str, position: tuple, char: str) -> None:
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
        self.char = char
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
            del self.map.entity_position[self.position]
            self.map.entity_position[value] = self
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

    def move(self, method: str) -> tuple:
        """
            Allows the entity to move in the map

            *param method: method to apply
            *type method: str
            *return: (old_position, next_position)
            *rtype: tuple
        """
        next_position = getattr(self, method, self.position)
        if self.check_move(next_position):
            old_position = self.position
            if next_position in self.map.entity_position:
                id = self.map.entity_position[next_position]
                char = id.char
                if char == PATH_CHAR:
                    self.pick_up(id)
                elif char == GUARD_CHAR:
                    self.meet_guard()
                elif char == STAIR_CHAR:
                    self.end_game()
            self.position = next_position
            return (old_position, next_position)
        return ()

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

    def meet_guard(self) -> None:
        """
            The player meet the guard: what's going on ?

            *return: None
        """
        if self.state >= ITEMS_NUMBER:
            print("You put the guard to sleep!")
        else:
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
