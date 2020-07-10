#coding: utf-8


# question à poser : utilisation des f' autorisée ? Requiert python 3.6+

"""Il n'y a qu'un seul niveau. La structure (départ, emplacement des murs, arrivée), devra être enregistrée dans un fichier pour la modifier facilement au besoin.
MacGyver sera contrôlé par les touches directionnelles du clavier.
Les objets seront répartis aléatoirement dans le labyrinthe et changeront d’emplacement si l'utilisateur ferme le jeu et le relance.
La fenêtre du jeu sera un carré pouvant afficher 15 sprites sur la longueur.
MacGyver devra donc se déplacer de case en case, avec 15 cases sur la longueur de la fenêtre !
Il récupèrera un objet simplement en se déplaçant dessus.
Le programme s'arrête uniquement si MacGyver a bien récupéré tous les objets et trouvé la sortie du labyrinthe. S'il n'a pas tous les objets et qu'il se présente devant le garde, il meurt (la vie est cruelle pour les héros).
Le programme sera standalone, c'est-à-dire qu'il pourra être exécuté sur n'importe quel ordinateur."""


import os
import pygame
from pygame.locals import *
from random import choice
from constants import *

class Item:
    """doc string : help(Item)"""
    """séparer les class dans différents fichiers, dans un sous-dossier"""
    def __init__(self, icon):
        image = pygame.image.load(icon)
        self.image = image
        self.is_item = True
        self.pos_x, self.pos_y = random_position()
        map.items.append(self)

        # object placement
        self.position = image.get_rect()
        self.position = self.position.move(self.pos_x * CASE_SIZE, self.pos_y * CASE_SIZE)

def random_position():
    """The position of the objets is random.
    Two objects can't have the same position.
    The location must be available."""
    # OU ??
    # nb = randrange(len(map.empty_case))
    # return map.empty_case.pop(nb)

    nb = choice(map.empty_case)
    map.empty_case.remove(nb)
    return nb

class Character:
    def __init__(self):
        self.is_item = False

        image = pygame.image.load(IMAGE_PJ).convert_alpha()
        self.image = image
        self.pos_x, self.pos_y = map.PJ_initial_position
        self.position = image.get_rect()
        self.position = self.position.move(self.pos_x * CASE_SIZE, self.pos_y * CASE_SIZE)
        map.items.append(self)

    def move(self, direction):
        is_moving = False

        if direction == K_RIGHT:
            is_moving = self.check_move(1, 0)
        elif direction == K_LEFT:
            is_moving = self.check_move(-1, 0)
        elif direction == K_UP:
            is_moving = self.check_move(0, -1)
        elif direction == K_DOWN:
            is_moving = self.check_move(0, 1)

        if is_moving:
            for item in map.items: # collision
                if self != item and item.is_item and self.position.contains(item.position): # no collision with himself
                #if self != item and self.pos_x == item.pos_x and self.pos_y == item.pos_y:
                    self.pick_up(item)

            if map.sprite(self.pos_x, self.pos_y) == 'G': # guard
                if self.state == 3: # 3 objets en sa possession
                    print("Vous endormissez le garde !")
                    self.state = 4
                elif self.state < 3:
                    print("Le garde vous vois ! C'est la mort !")
                    self.state = 9
            elif map.sprite(self.pos_x, self.pos_y) == 'S': # + vérif ou endormissement gardien
                print("Vous vous échappez du labyrinthe ! Fin de partie !")
                self.state = 8


    def check_move(self, x, y):
        """this function checks the new position of the player
        return False if :
            the game is over or PJ is dead
            or new position aren't in the MAP_SIZE
            or new position is a Wall
        else:
            new position is saved
            window is refreshed
        """
        next_x = self.pos_x + x
        next_y = self.pos_y + y
        
        if self.state > 7:
            return False
        elif next_x < 0 or next_y < 0:
            return False
        elif next_x >= MAP_SIZE or next_y >= MAP_SIZE:
            return False
        elif map.sprite(next_x, next_y) == 'W':
            return False

        self.position = self.position.move(x * CASE_SIZE, y * CASE_SIZE)
        self.pos_x = next_x
        self.pos_y = next_y
        window.blit()
 
        return True

    def pick_up(self, item):
        """if PJ and item position are the same
        item is removed from the ground
        self.state is incremented
        window is refreshed"""
        print("Great job! You found an object.")
        if self.state < 3:
            self.state += 1
        if self.state == 3:
            print("Vous fabriquez une serringue pour endormir le garde !")
        map.items.remove(item)
        window.blit()

class Map:
    def __init__(self):
        pass

    def init_Map(self): # square map
        """ Map's initialisation, detection of possibles errors"""

        if os.path.exists(MAP_NAME):
            with open(MAP_NAME, "r", encoding = "utf-8") as map_file:
                map_line = map_file.readlines()
                if len(map_line) < MAP_SIZE: # width check
                    print(f"Map file : width error, map must be more longer than {MAP_SIZE} not {len(map_line)}")
                    return None

                self.structure = []
                self.items = []
                self.empty_case = []
                nb_D = 0 # number of departure case
                nb_G = 0 # number of guard case
                nb_S = 0 # number of stair case

                for y, line in enumerate(map_line[:MAP_SIZE]): # seules les size premières lignes sont lues, ce qui peut permettre des commenter chaque fichier, lecture moins punitive
                    if len(line) < MAP_SIZE:
                        print(f"Map file : height error, height must be more longer than {MAP_SIZE} not {len(line)}")
                        return None

                    line = list(line[:MAP_SIZE].upper())
                    nb_D += line.count('D') # pourquoi pas une liste plate ?
                    nb_G += line.count('G')
                    nb_S += line.count('S')

                    for x, letter in enumerate(line):
                        if letter == 'O': # case libre
                            self.empty_case.append((x, y))
                        elif letter == 'D': # departure
                            self.PJ_initial_position = (x, y)

                    self.structure.append(line) # seuls les size premiers caractères sont lus, la chaîne de caractère est automatiquement convertie en list

                if nb_D != 1: # no departure or too many
                    print(f"Number departure error, {MAP_NAME} need one only case with D.")
                    return None
                elif nb_G < 1: # no guard
                    print(f"{MAP_NAME} need a Guard case (G) !")
                    return None
                elif nb_S < 1: # no stair
                    print(f"{MAP_NAME} need a Stair case (S) !")
                    return None
                elif len(self.empty_case) < 3: # not enough free case
                    print(f"{MAP_NAME} need three or more free cases (A) for items !")
                    return None

                print(f"{MAP_NAME} initialisation.")
        else:
            print(f"{MAP_NAME} not found.")
            return None

        return 1

    def sprite(self, x, y):
        return self.structure[y][x] # /!\

class Game_window:
    def __init__(self):
        if WINDOW_SIZE < 1:
            print(f"WINDOW_SIZE error, must be superior than 0.")
            return None

        self.id = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE)) # initialisation de la fenêtre
        self.background = pygame.image.load(IMAGE_BACKGROUND).convert() # chargement de l'image + conversion dans les dimensions adéquates
        self.wall = pygame.image.load(IMAGE_WALL)
        self.guard = pygame.image.load(IMAGE_GUARD)
        self.stair = pygame.image.load(IMAGE_STAIR)
        self.departure = pygame.image.load(IMAGE_DEPARTURE)

    def blit(self):
        self.id.blit(self.background, (0, 0)) # collage de l'image de fond

        for height, line in enumerate(map.structure):
            for width, letter in enumerate(line):
                target = None
                if letter == 'W': # wall
                    target = self.wall
                elif letter == 'G': # guard
                    target = self.guard
                elif letter == 'S': # stair
                    target = self.stair
                elif letter == 'D': # departure
                    target = self.departure

                if target:
                    self.id.blit(target, (width * CASE_SIZE, height * CASE_SIZE))

        for item in map.items:
            self.id.blit(item.image, item.position)

        pygame.display.flip() # rafraîchissement de la fenêtre
        # possibilité de rafraîchir que les cases ayant changé d'état ?

map = Map()
init = map.init_Map()
window = Game_window()
if init:
    player = Character()
    player.state = 0 # 1 : 1 objet, 2 : 2 objets, 3 : 3 objets, 4 : garde endormi, 9 : mort, 8 : fin de labyrinthe

    Item(IMAGE_ETHER)
    Item(IMAGE_TUBE)
    Item(IMAGE_NEEDLE)

    window.blit()

    continuer = True

    while continuer:
        pygame.time.Clock().tick(30) # limitation à 30 boucles/seconde
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer = False
            elif event.type == KEYDOWN and event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                player.move(event.key)

#os.system("pause")