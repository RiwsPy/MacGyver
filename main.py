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
from classes import *

def main():
    # game window initialisation
    window.Game_window()
    level = map.Map()

    if level.check_Map():
        entity.generate_entity()
        window.game_loop()


if __name__ == "__main__":
    main()