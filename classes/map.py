#coding: utf-8

import os
from classes.locale import MAP_NAME, ITEM_NUMBER, MAP_SIZE, IMAGE_PJ, IMAGE_ETHER, IMAGE_TUBE, IMAGE_NEEDLE
import classes.entity


class Map:
    def __init__(self) -> None:
        self.structure = []
        self.items = []
        self.empty_case = []
        self.PJ_initial_position = None
        
    def check_Map(self, window_id, map_id) -> bool: # square map
        """ Map initialisation & map check """

        if os.path.exists(MAP_NAME):
            with open(MAP_NAME, "r", encoding = "utf-8") as map_file:
                map_line = map_file.readlines()
                if len(map_line) < MAP_SIZE: # width check
                    print(f"Map file : width error, map must be more longer than {MAP_SIZE} not {len(map_line)}")
                    return False

                if ITEM_NUMBER < 1 or ITEM_NUMBER > 6:
                    print("locale file : ITEM_NUMER error, must be in [1, 6]")
                    return False

                nb_G = 0
                nb_S = 0

                for y, line in enumerate(map_line[:MAP_SIZE]): # seules les size premières lignes sont lues, ce qui peut permettre des commenter chaque fichier, lecture moins punitive
                    if len(line) < MAP_SIZE:
                        print(f"Map file : height error, height must be more longer than {MAP_SIZE} not {len(line)}")
                        return False

                    line = list(line[:MAP_SIZE].upper())
                    self.structure.append(line) # seuls les size premiers caractères sont lus, la chaîne de caractère est automatiquement convertie en list

                    for x, letter in enumerate(line):
                        if letter == 'O': # case libre
                            self.empty_case.append((x, y))
                        elif letter == 'W': 
                            continue
                        elif letter == 'D' : # departure
                            self.PJ_initial_position = (x, y)
                        elif letter == 'S':
                            nb_S += 1
                        elif letter == 'G':
                            nb_G += 1
                        else: 
                            self.empty_case.append((x, y))

                if self.PJ_initial_position is None: # no departure
                    print(f"Number departure error, {MAP_NAME} need one only case with D.")
                    return False
                elif nb_G < 1: # no guard
                    print(f"{MAP_NAME} need a Guard case (G) !")
                    return False
                elif nb_S < 1: # no stair
                    print(f"{MAP_NAME} need a Stair case (S) !")
                    return False
                elif len(self.empty_case) < ITEM_NUMBER: # not enough free case
                    print(f"{MAP_NAME} need three or more free cases (A) for items !")
                    return False

                print(f"{MAP_NAME} initialisation.")
        else:
            print(f"{MAP_NAME} not found.")
            return False

        classes.entity.Entity(self, IMAGE_PJ, is_item = False)
        classes.entity.Entity(self, IMAGE_ETHER)
        classes.entity.Entity(self, IMAGE_TUBE)
        classes.entity.Entity(self, IMAGE_NEEDLE)

        window_id.refresh_window(map_id)
        return True

    def sprite(self, x: int, y: int) -> str:
        """ returns the letter of the coordinate pair (x, y)"""
        return self.structure[y][x] # /!\
        
    def my_sprite(self, id) -> str:
        """ return the letter to the entity's position"""
        return self.structure[id.pos_y][id.pos_x]