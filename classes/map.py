# coding: utf-8

"""
    Class to manage the Map
"""

import os
from classes.locale import MAP_NAME, ITEMS_NUMBER, MAP_SIZE, IMAGE_PJ, \
    IMAGE_ITEM_1, IMAGE_ITEM_2, IMAGE_ITEM_3, \
    IMAGE_ITEM_4, IMAGE_ITEM_5, IMAGE_ITEM_6
import classes.entity


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
        self.empty_case = []
        self.PJ_initial_position = None

    def check_Map(self, window_id) -> bool:  # square map
        """
            Map check errors

            *param window_id: window id
            *type id: window.WindowManager
            *return: False if an error is occurred
                during the map load, True otherwise
            *rtype: bool
        """
        if os.path.exists(MAP_NAME):
            with open(MAP_NAME, "r", encoding="utf-8") as map_file:
                map_line = map_file.readlines()
                if len(map_line) < MAP_SIZE:  # width check
                    print(f"Map file : width error, map must be more longer than\
                        {MAP_SIZE} not {len(map_line)}")
                    return False

                nb_G = 0
                nb_S = 0

                for y, line in enumerate(map_line[:MAP_SIZE]):
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
                        if letter == 'O':  # empty case
                            self.empty_case.append((x, y))
                        elif letter == 'W':
                            continue
                        elif letter == 'D':  # departure
                            self.PJ_initial_position = (x, y)
                        elif letter == 'S':  # stair
                            nb_S += 1
                        elif letter == 'G':  # guard
                            nb_G += 1
                        else:  # defaut case is an empty case
                            self.empty_case.append((x, y))

                if self.PJ_initial_position is None:  # no departure
                    print(f"Number departure error, {MAP_NAME}\
                        needs one only case with D.")
                    return False
                elif nb_G < 1:  # no guard
                    print(f"{MAP_NAME} needs a Guard case (G) !")
                    return False
                elif nb_S < 1:  # no stair
                    print(f"{MAP_NAME} needs a Stair case (S) !")
                    return False
                elif len(self.empty_case) < ITEMS_NUMBER:
                    # not enough free case
                    print(f"{MAP_NAME} needs {ITEMS_NUMBER} \
                        or more free cases (A) for items !")
                    return False

                print(f"{MAP_NAME} initialisation.")
        else:
            print(f"{MAP_NAME} not found.")
            return False

        # generate PJ
        classes.entity.EntityManager(window_id, self, IMAGE_PJ, is_item=False)

        # generate items
        if ITEMS_NUMBER > 6 or ITEMS_NUMBER < 1:
            print("locale file : ITEM_NUMBER error, must be in [1, 6]")
            return False

        item_name_list = [IMAGE_ITEM_1, IMAGE_ITEM_2, IMAGE_ITEM_3,
                          IMAGE_ITEM_4, IMAGE_ITEM_5, IMAGE_ITEM_6]
        for i in range(ITEMS_NUMBER):
            if item_name_list[i] is None:
                print(f"locale file : error : IMAGE_ITEM_{i} is None")
                return False

            classes.entity.EntityManager(window_id, self, item_name_list[i],
                                  is_item=True)

        window_id.refresh_window(self)
        return True

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
