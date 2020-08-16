# coding: utf-8

"""
    Class to manage the Map
"""

import os
from classes.locale import ITEMS_NUMBER, MAP_SIZE, IMAGE_PJ, \
    IMAGE_ITEM_1, IMAGE_ITEM_2, IMAGE_ITEM_3, \
    IMAGE_ITEM_4, IMAGE_ITEM_5, IMAGE_ITEM_6, \
    PATH_CHAR, GUARD_CHAR, STAIR_CHAR, WALL_CHAR, DEPARTURE_CHAR
from classes.entity import EntityManager
from random import choice


class MapManager:
    """
        Class to create the map
    """
    def __init__(self) -> None:
        """
            Map initialisation
        """
        self.structure = []
        self.items = []
        self.empty_case = set()
        self.start_position = tuple()

    def load_from_file(self, map_file) -> bool:  # square map
        """
            Map check errors

            *param map_file: map's file name
            *type map_file: str
            *return: False if an error is occurred
                during the map load, True otherwise
            *rtype: bool
        """
        if os.path.exists(map_file):
            with open(map_file, "r", encoding="utf-8") as open_map_file:
                lines = open_map_file.readlines()
                if len(lines) < MAP_SIZE:  # width check
                    print(f"Map file : width error, map must be more longer than\
                        {MAP_SIZE} not {len(lines)}")
                    return False

                nb_G = 0
                nb_S = 0

                for y, line in enumerate(lines[:MAP_SIZE]):
                    """ only the first lines are read
                    which can allow comments on each file
                    less punitive reading """
                    if len(line) < MAP_SIZE:
                        print(f"Map file : height error, height must be more longer than\
                            {MAP_SIZE} not {len(line)}")
                        return False

                    line = list(line[:MAP_SIZE].upper())
                    self.structure.append(line)

                    for x, letter in enumerate(line):
                        if letter == PATH_CHAR:
                            self.empty_case.add((x, y))
                        elif letter == WALL_CHAR:
                            continue
                        elif letter == DEPARTURE_CHAR:
                            self.start_position = (x, y)
                        elif letter == STAIR_CHAR:
                            nb_S += 1
                        elif letter == GUARD_CHAR:
                            nb_G += 1
                        else:  # defaut case is a path case
                            self.empty_case.add((x, y))

                if self.start_position == ():  # no departure
                    print(f"Number departure error, {map_file}\
                        needs one case with {DEPARTURE_CHAR}.")
                    return False
                elif nb_G < 1:  # no guard
                    print(f"{map_file} needs a Guard case {GUARD_CHAR} !")
                    return False
                elif nb_S < 1:  # no stair
                    print(f"{map_file} needs a Stair case {STAIR_CHAR} !")
                    return False
                elif len(self.empty_case) < ITEMS_NUMBER:
                    # not enough free case
                    print(f"{map_file} needs {ITEMS_NUMBER} \
                        or more free cases {PATH_CHAR} for items !")
                    return False

                print(f"{map_file} initialisation.")
        else:
            print(f"{map_file} not found.")
            return False

        return self.generate_entities()

    def generate_entities(self):
        """
            Generate Player and items
        """
        # generate PJ
        player = EntityManager(self, IMAGE_PJ,
                               position=self.start_position)
        self.items.append(player)

        # generate items
        if ITEMS_NUMBER > 6 or ITEMS_NUMBER < 1:
            print("locale file : ITEM_NUMBER error, must be in [1, 6]")
            return False

        item_name_list = [IMAGE_ITEM_1, IMAGE_ITEM_2, IMAGE_ITEM_3,
                          IMAGE_ITEM_4, IMAGE_ITEM_5, IMAGE_ITEM_6]
        for i in range(ITEMS_NUMBER):
            if item_name_list[i] is None:
                print(f"locale file : value error : IMAGE_ITEM_{i} is None")
                return False

            item = EntityManager(self, item_name_list[i],
                                 position=self.random_position())
            self.items.append(item)

        return player

    def sprite(self, x: int, y: int) -> str:
        """
            returns the letter of the coordinate pair (x, y)

            *param x: x-axis
            *param y: y-axis
            *type x: int
            *type y: int
            *return: the letter of map file
            *rtype: str
        """
        return self.structure[y][x]  # /!\

    def my_sprite(self, id) -> str:
        """
            return the letter to the entity's position

            *param id: entity id
            *type id: entity.EntityManager
            *return: the map letter to
                the player's coordinates
            *rtype: str
        """
        return self.structure[id.pos_y][id.pos_x]

    def random_position(self) -> tuple:
        """
            Object's position is randomly chosen
            Two objects can't have the same position
            The location must be available

            *return: (x-axis, y-axis)
            *rtype: tuple
        """
        nb = choice(tuple(self.empty_case))
        self.empty_case.discard(nb)
        return nb

    def is_valid_position(self, position: tuple) -> bool:
        """
            Return True if the position (x, y) is valid for move,
            False otherwise
            *param position: position to check
            *type position: tuple
            *rtype: bool
        """
        next_x, next_y = position
        if next_x < 0 or next_x >= MAP_SIZE:
            return False
        if next_y < 0 or next_y >= MAP_SIZE:
            return False
        if self.sprite(next_x, next_y) == WALL_CHAR:
            return False

        return True
