# coding: utf-8

"""
    Class to manage the Map
"""

import os
from config.locale import ITEMS_NUMBER, MAP_SIZE, \
    items_icon, PATH_CHAR, START_CHAR, letter_to_icon
from game.entity import EntityManager
from random import choice


class MapManager:
    """
        Class to create the map
    """
    def __init__(self) -> None:
        """
            Map initialisation
        """
        self.path_position = set()
        self.entity_position = {}

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
                # player id
                player = None

                for y, line in enumerate(lines[:MAP_SIZE]):
                    """ only the first lines are read
                    which can allow comments on each file
                    less punitive reading """

                    line = line[:MAP_SIZE].upper()
                    for x, letter in enumerate(line):
                        if letter in letter_to_icon:
                            self.path_position.add((x, y))
                            if letter != PATH_CHAR:
                                id = EntityManager(self,
                                                   letter_to_icon[letter],
                                                   position=(x, y),
                                                   char=letter)
                                self.entity_position[(x, y)] = id
                                if letter == START_CHAR:
                                    player = id

                if player is None:  # no departure
                    print(f"Start case error, {map_file}\
                        needs one case with {START_CHAR}.")
                    return None
                if ITEMS_NUMBER > (len(self.path_position) -
                                   len(self.entity_position)):
                    print(f"{map_file} needs {ITEMS_NUMBER} \
                        or more free cases {PATH_CHAR} for items !")
                    return None

                print(f"{map_file} initialisation.")
                self.generate_items()
                return player

        print(f"{map_file} not found.")
        return None

    def generate_items(self) -> None:
        """
            Generate items
            *return: None
        """
        # generate items
        if ITEMS_NUMBER > len(items_icon):
            print("locale file : items_icon error, contains not enough items")
            return None

        empty_case = self.path_position - set(self.entity_position.keys())
        empty_case = list(empty_case)

        for i in range(ITEMS_NUMBER):
            if items_icon[i] is None:
                print(f"locale file : value error : items_icon[{i}] is None")
                return None

            item_position = self.random_position(empty_case)
            id = EntityManager(self, icon=items_icon[i],
                               position=item_position,
                               char=PATH_CHAR)

            self.entity_position[item_position] = id

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
        return position in self.path_position
