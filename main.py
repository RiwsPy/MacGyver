#coding: utf-8

"""
Labyrinthe game : MacGyver must escape !

Script Python
Files:
------
"""


# question à poser : utilisation des f' autorisée ? Requiert python 3.6+
# d'ailleurs, où les dépendances sont à indiquer ? main.py ?

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
    > pas certain de l'intérêt actuel
* Facultatif : Utiliser les types hints ?
    > atchoum ? > annotation des functions

"""

import os
import pygame
from classes import *
from pygame.locals import *
import locale

global L, L2
L = ["o", "k", ["o"], ["k", [3, 4]], "o", [[2, 3, [1, 7]]]]
L2 = []

def main2(arg = L) -> None:
    for value in arg:
        if type(value) is list:
            main2(value)
        else:
            L2.append(value)

    if arg == L:
        print(L2)


def main4() -> None:
    import timeit
    print(timeit.timeit("""
a = [["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"]]
new = []
for line in a:
    new.extend(line)
""", number = 10000))

    print(timeit.timeit("""
a = [["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"]]
new = []
for line in a:
    new.append(line)
""", number = 10000))

    print(timeit.timeit("""
a = [["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"]]
new = []
for line in a:
    new += line
""", number = 10000))


def main3() -> None:
    import timeit
    print(timeit.timeit(
"""
O = []
nb_o, nb_k, nb_m = 0, 0, 0
a = [["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"]]
for line in a:
    for letter in line:
        O.append(letter)
nb_o += O.count("o")
nb_k += O.count("k")
nb_m += O.count("m")""", number=10000))


    print(timeit.timeit(
"""
O = []
nb_o, nb_k, nb_m = 0, 0, 0
a = [["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"], ["o", "k", "l", "m", "n", "o"]]
for line in a:
    nb_o += line.count("o")
    nb_k += line.count("k")
    nb_m += line.count("m")
    for letter in line:
        O.append(letter)
""", number=10000))



def main() -> None:
    # game window initialisation
    window.Game_window()
    level = map.Map()

    if level.check_Map():
        entity.generate_entity()
        game_loop()


def game_loop() -> None:
    continuer = True

    while continuer:
        pygame.time.Clock().tick(30) # limitation à 30 boucles/seconde
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer = False
            elif event.type == KEYDOWN and event.key in [K_RIGHT, K_LEFT, K_UP, K_DOWN]:
                locale.PLAYER.move(event.key)


if __name__ == "__main__":
    main()
    #os.system("pause")
