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

""" 
les conseils d'Olivier :

* Faire un fichier "main" avec à l’intérieur un  if __name__ == '__main__'
* Séparer les classes en fichiers et les mettres dans un sous dossier et y ajouter un __init__.py
* Facultatif : Utiliser les types hints ?
    > what ?

"""


import os
import pygame
from locale import *
from classes import *
from pygame.locals import *

# game loop function ?
class GameManager:
    def __init__(self):
        level = map.Map()
        init = level.init_Map()
        game_window = window.Game_window()
        if init:
            global player
            player = entity.Entity(IMAGE_PJ)

            entity.Entity(IMAGE_ETHER, is_item = True)
            entity.Entity(IMAGE_TUBE, is_item = True)
            entity.Entity(IMAGE_NEEDLE, is_item = True)

            game_window.refresh()
            self.game_loop()

    def game_loop(self):
        continuer = True

        while continuer:
            pygame.time.Clock().tick(30) # limitation à 30 boucles/seconde
            for event in pygame.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer = False
                elif event.type == KEYDOWN and event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                    player.move(event.key)

        #os.system("pause")