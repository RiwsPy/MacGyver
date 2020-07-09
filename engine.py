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
import random


MAP_SIZE = 15

class Main:
    def __init__(self, image, position = None):
        self.is_item = False
        if position is None:
            self.is_item = True
            position = random_position()

        if position[0] < 0 or position[1] < 0 or position[0] >= MAP_SIZE or position[1] >= MAP_SIZE:
            print(f"Object {image} position error")
            return None

        id = pygame.image.load(image).convert_alpha()
        global map_items
        self.id = id
        self.position = id.get_rect()
        self.position = self.position.move(position[0]*32, position[1]*32)
        map_items.append(self)
        self._x, self._y = position

    @property
    def x(self):
        return self._x
        
    @x.setter
    def x(self, value):
        if self._x != value:
            self.position = self.position.move((value - self._x) * 32, 0)
            self._x = value
            window_blit()

    @property
    def y(self):
        return self._y
        
    @y.setter
    def y(self, value):
        if self._y != value:
            self.position = self.position.move(0, (value - self._y) * 32)
            self._y = value
            window_blit()

    def move(self, direction):
        if direction == K_RIGHT:
            self.check_move(self.x+1, self.y)
                
        elif direction == K_LEFT:
            self.check_move(self.x-1, self.y)

        elif direction == K_UP:
            self.check_move(self.x, self.y-1)

        elif direction == K_DOWN:
            self.check_move(self.x, self.y+1)

        for item in map_items: # collision
            if self.position.contains(item.position) and self != item:
                if item.is_item:
                    print("objet trouvé")
                    self.state += 1
                    if self.state == 3:
                        print("Vous créez une serringue pour endormir le garde !")
                    map_items.remove(item)
                    window_blit()

        if map_list[self.y][self.x] == 'G': # gardien
            if self.state == 3: # 3 objets en sa possession
                print("Vous endormissez le gardien !")
                self.state = 4
            elif item.state < 3:
                print("Le gardien vous vois ! C'est la mort !")
                self.state = 9
        elif map_list[self.y][self.x] == 'S':
            print("Vous vous échappez du labyrinthe ! Fin de partie !")
            self.state = 8

    def check_move(self, posX, posY):
        if self.state > 7:
            return False
        if posX < 0 or posY < 0:
            return False
        if posX >= MAP_SIZE or posY >= MAP_SIZE:
            return False
        if map_list[posY][posX] == 'W': # /!\
            return False

        self.x = posX
        self.y = posY

def init_Map(map_name = "map.py"): # square map
    if MAP_SIZE < 1: # limite supérieure ?
        print("Map size error, must be positive.")
        return None

    if os.path.exists(map_name):
        with open(map_name, "r", encoding = "utf-8") as map_file:
            map_line = map_file.readlines()
            global map_list
            map_list = []
            if len(map_line) < MAP_SIZE: # width check
                print(f"Map file : width error, map must be more longer than {size} not {len(map_line)}")
                return None

            for line in map_line[:MAP_SIZE]: # seules les size premières lignes sont lues, ce qui peut permettre des commenter chaque fichier, lecture moins punitive
                if len(line) < MAP_SIZE+1: # size + \n, height check
                    print(f"Map file : height error, height must be more longer than {MAP_SIZE+1} not {len(line)}")
                    return None
                map_list.append(list(line[:MAP_SIZE])) # seuls les size premiers caractères sont lus, la chaîne de caractère est automatiquement convertie en list

            print("Map file initialisation.")
    else:
        print("Map file not found.")
        return None
    init_Window()

def init_Window():
    global window, background, wall, map_items, guardian, stair

    window = pygame.display.set_mode((MAP_SIZE*32, MAP_SIZE*32)) # initialisation de la fenêtre
    background = pygame.image.load("ressource/background.jpg").convert() # chargement de l'image + conversion dans les dimensions adéquates
    wall = pygame.image.load("ressource/wall.png").convert_alpha()
    guardian = pygame.image.load("ressource/Garde.png").convert_alpha()
    stair = pygame.image.load("ressource/Stair.png").convert_alpha()
    map_items = []


def window_blit():
    window.blit(background, (0, 0)) # collage de l'image de fond

    for height, line in enumerate(map_list):
        for width, letter in enumerate(line):
            if letter == 'W': # wall
                window.blit(wall, (width*32, height*32))
            elif letter == 'G': # guardian
                window.blit(guardian, (width*32, height*32))
            elif letter == 'S': # stairs
                window.blit(stair, (width*32, height*32))

    for item in map_items:
        window.blit(item.id, item.position)

    pygame.display.flip() # rafraîchissement de la fenêtre
    # possibilité de rafraîchir que les cases ayant changé d'état ?

# position aléatoire à déterminer, excepté : position initiale de player, celle du gardien, ceux des murs, ceux des autres items
# vérification des cases pour déterminer si le terrain est rempli de murs ?
def random_position():
    continuer = True
    while continuer:
        continuer = False
        nb1 = random.randrange(MAP_SIZE)
        nb2 = random.randrange(MAP_SIZE)
        if map_list[nb2][nb1] == 'A': # ne check que les cases libres
            for item in map_items: # pas de cumul des objets sur la même case
                if item.x == nb1 and item.y == nb2:
                    continuer = True
                    break
        else:
            continuer = True
    return nb1, nb2


init_Map()

player = Main(image = "ressource/PJ.png", position = (0, 0))
player.state = 0 # 1 : 1 objet, 2 : 2 objets, 3 : 3 objets, 4 : garde endormi, 9 : mort, 8 : fin de labyrinthe

Main("ressource/ether2.png")
Main("ressource/tube.png")
Main("ressource/tube.png")

window_blit()

continuer = 1

# gestion fenêtre



while continuer:
    pygame.time.Clock().tick(30) # limitation à 30 boucles/seconde
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:     #Si un de ces événements est de type QUIT
            continuer = 0
        elif player.state < 8 and event.type == KEYDOWN and event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
            player.move(event.key)

#os.system("pause")