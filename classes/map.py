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
        self.structure = {}
        self.items = []
        self.start_position = ()
        self.guard_position = ()
        self.stair_position = ()

    def load_from_file(self, map_file: str):  # square map
        """
            Map check errors

            *param map_file: map's file name
            *type map_file: str
            *return: None if an error is occurred
                during the map load, player id otherwise
            *rtype: entity.EntityManager
        """
        if os.path.exists(map_file):
            with open(map_file, "r", encoding="utf-8") as open_map_file:
                lines = open_map_file.readlines()
                if len(lines) < MAP_SIZE:  # width check
                    print(f"Map file : width error, map must be more longer than\
                        {MAP_SIZE} not {len(lines)}")
                    return None

                empty_case = 0

                for y, line in enumerate(lines[:MAP_SIZE]):
                    """ only the first lines are read
                    which can allow comments on each file
                    less punitive reading """
                    if len(line) < MAP_SIZE:
                        print(f"Map file : height error, height must be more longer than\
                            {MAP_SIZE} not {len(line)}")
                        return None

                    line = line[:MAP_SIZE].upper()
                    for x, letter in enumerate(line):
                        if letter == PATH_CHAR:
                            empty_case += 1
                            self.structure[(x, y)] = letter
                        elif letter == DEPARTURE_CHAR:
                            self.start_position = (x, y)
                            self.structure[(x, y)] = letter
                        elif letter == STAIR_CHAR:
                            self.stair_position = (x, y)
                            self.structure[(x, y)] = letter
                        elif letter == GUARD_CHAR:
                            self.guard_position = (x, y)
                            self.structure[(x, y)] = letter

                if self.start_position == ():  # no departure
                    print(f"Number departure error, {map_file}\
                        needs one case with {DEPARTURE_CHAR}.")
                    return None
                elif self.guard_position == ():  # no guard
                    print(f"{map_file} needs a Guard case {GUARD_CHAR} !")
                    return None
                elif self.stair_position == ():  # no stair
                    print(f"{map_file} needs a Stair case {STAIR_CHAR} !")
                    return None
                elif empty_case < ITEMS_NUMBER:
                    # not enough free case
                    print(f"{map_file} needs {ITEMS_NUMBER} \
                        or more free cases {PATH_CHAR} for items !")
                    return None

                print(f"{map_file} initialisation.")
        else:
            print(f"{map_file} not found.")
            return None

        return self.generate_entities()

    def generate_entities(self):
        """
            Generate Player and items
            *return: player id
            *rtype: entity.EntityManager
        """
        # generate PJ
        player = EntityManager(self, IMAGE_PJ,
                               position=self.start_position)
        self.items.append(player)

        # generate items
        if ITEMS_NUMBER > 6 or ITEMS_NUMBER < 1:
            print("locale file : ITEM_NUMBER error, must be in [1, 6]")
            return None

        item_name_list = [IMAGE_ITEM_1, IMAGE_ITEM_2, IMAGE_ITEM_3,
                          IMAGE_ITEM_4, IMAGE_ITEM_5, IMAGE_ITEM_6]
        empty_case = self.structure.copy()
        empty_case[self.start_position] = None
        empty_case[self.stair_position] = None
        empty_case[self.guard_position] = None
        empty_case = list(empty_case)

        for i in range(ITEMS_NUMBER):
            if item_name_list[i] is None:
                print(f"locale file : value error : IMAGE_ITEM_{i} is None")
                return None

            item = EntityManager(self, item_name_list[i],
                                 position=self.random_position(empty_case))
            self.items.append(item)

        return player

    def sprite(self, position: tuple) -> str:
        """
            returns letter of the position in structure

            *param position: (x-axis, y-axis)
            *type x: tuple
            *return: the letter of map file
            *rtype: str
        """
        return self.structure.get(position, WALL_CHAR)

    def random_position(self, empty_case: list) -> tuple:
        """
            Object's position is randomly chosen
            Two objects can't have the same position
            The location must be available

            *param empty_case: list of possible case
            *type empty_case: list
            *return: (x-axis, y-axis)
            *rtype: tuple
        """
        nb = choice(empty_case)
        empty_case.remove(nb)
        return nb

    def is_valid_position(self, position: tuple) -> bool:
        """
            Return True if the position (x, y) is valid for move,
            False otherwise
            *param position: position to check
            *type position: tuple
            *rtype: bool
        """
        return self.sprite(position) != WALL_CHAR
