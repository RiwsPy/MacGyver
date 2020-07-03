#coding: utf-8


"""Il n'y a qu'un seul niveau. La structure (départ, emplacement des murs, arrivée), devra être enregistrée dans un fichier pour la modifier facilement au besoin.
MacGyver sera contrôlé par les touches directionnelles du clavier.
Les objets seront répartis aléatoirement dans le labyrinthe et changeront d’emplacement si l'utilisateur ferme le jeu et le relance.
La fenêtre du jeu sera un carré pouvant afficher 15 sprites sur la longueur.
MacGyver devra donc se déplacer de case en case, avec 15 cases sur la longueur de la fenêtre !
Il récupèrera un objet simplement en se déplaçant dessus.
Le programme s'arrête uniquement si MacGyver a bien récupéré tous les objets et trouvé la sortie du labyrinthe. S'il n'a pas tous les objets et qu'il se présente devant le garde, il meurt (la vie est cruelle pour les héros).
Le programme sera standalone, c'est-à-dire qu'il pourra être exécuté sur n'importe quel ordinateur."""


import os


class Main:
	def __init__(self):
		self.init_Player()

	def init_PNJ(self, name, position):
		self.name = name
		self.position = position
		self.hp = 1 # only one hp
		self.state = 0 # 1 : sleeping
		self.inventory = [] # empty

	def init_Player(self, name = "MacGyver", position = (0, 0)):
		self.init_PNJ(name, position)
		global player
		player = self

	def init_Map(self, size = 15): # square map
		pass

Main()
print(player.name)

os.system("pause")