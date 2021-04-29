import pygame, math, random
from pygame.locals import *

#Les couleurs a utiliser
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

#Les dimensions de la fenetre qui affiche
TAILLEFENETRE = (500, 500)
TAILLEFENETRE_X = TAILLEFENETRE[0]
TAILLEFENETRE_Y = TAILLEFENETRE[1]

#Les dimensions de la cellule
TAILLECARRE = 25
NMBCASEX = 25
NMBCASEY = 25

#Rapidite de l'image (Quand on utilise play et pause)
FPS = 60
clock = pygame.time.Clock()

#Initialisation de PYGAME
pygame.init()
fenetre = pygame.display.set_mode(TAILLEFENETRE)

class Cell:
	def __init__(self, x, y, state):
		self.x = x
		self.y = y
		self.state = state #0 si elle est morte et 1 si elle est vivante
		self.nmbVoisine = 0 #pour calculer la somme des nbrs voisines

	#Fonction pour trouver le nombre des cellules voisines qui prend en parametre numbX et numbY qui sont les coordonées de la cellule courante
	def voisine(self, listCells, nmbX, nmbY):
		voisine = 0
		if self.x+1<nmbX:
			if listCells[self.x+1][self.y].state == 1:
				voisine += 1
		if 0<=self.x-1:
			if listCells[self.x-1][self.y].state == 1:
				voisine += 1
		if self.y+1<nmbY:
			if listCells[self.x][self.y+1].state == 1:
				voisine += 1
		if 0<=self.y-1:
			if listCells[self.x][self.y-1].state == 1:
				voisine += 1
		if self.x+1<nmbX and self.y+1<nmbY:
			if listCells[self.x+1][self.y+1].state == 1:
				voisine += 1
		if 0<=self.x-1 and self.y+1<nmbY:
			if listCells[self.x-1][self.y+1].state == 1:
				voisine += 1
		if 0<=self.x-1 and 0<=self.y-1:
			if listCells[self.x-1][self.y-1].state == 1:
				voisine += 1
		if self.x+1<nmbX and 0<=self.y-1:
			if listCells[self.x+1][self.y-1].state == 1:
				voisine += 1

		self.nmbVoisine = voisine

	def calcule(self):
		#Definire l'etat de la cellule selon les rules du jeu

		if self.state == 0:
			if self.nmbVoisine == 3:
				self.state = 1

		if self.state == 1:
			if self.nmbVoisine < 2:
				self.state = 0
			elif self.nmbVoisine == 2:
				self.state = 1
			elif self.nmbVoisine > 3:
				self.state = 0

	#Definition des lignes et des colonnes
	def draw(self, fenetre):
		if self.state == 0: #morte = BLANC
			pygame.draw.rect(fenetre, BLANC, (self.x * TAILLECARRE, self.y * TAILLECARRE, TAILLECARRE, TAILLECARRE), 0)
			pygame.draw.line(fenetre, NOIR, (self.x * TAILLECARRE, self.y * TAILLECARRE), (self.x * TAILLECARRE+TAILLECARRE, self.y * TAILLECARRE), 1)
			pygame.draw.line(fenetre, NOIR, (self.x * TAILLECARRE, self.y * TAILLECARRE), (self.x * TAILLECARRE, self.y * TAILLECARRE+TAILLECARRE), 1)
			pygame.draw.line(fenetre, NOIR, (self.x * TAILLECARRE, self.y * TAILLECARRE+TAILLECARRE), (self.x * TAILLECARRE+TAILLECARRE, self.y * TAILLECARRE+TAILLECARRE), 1)
			pygame.draw.line(fenetre, NOIR, (self.x * TAILLECARRE+TAILLECARRE, self.y * TAILLECARRE), (self.x * TAILLECARRE+TAILLECARRE, self.y * TAILLECARRE+TAILLECARRE), 1)
		if self.state == 1: #vivante = NOIRE
			pygame.draw.rect(fenetre, NOIR, (self.x * TAILLECARRE, self.y * TAILLECARRE, TAILLECARRE, TAILLECARRE), 0)
			

class World:
	def __init__(self, nmbX, nmbY):
		self.nmbX = nmbX
		self.nmbY = nmbY
		self.listCells = []
		self.gen = 0

	def init(self):
		for x in range(self.nmbX):
			self.listCells.append([])

		#Initialization des cellules avant que le jeu commence par default, toutes les celllues sont mortes 
		for x in range(self.nmbX):
			for y in range(self.nmbY):
				newCell = Cell(x,y,0)
				#La liste listCells contient toutes les cellules
				self.listCells[x].append(newCell)
				
		for x in range(len(self.listCells)):
			for y in range(len(self.listCells[x])):
				self.listCells[x][y].voisine(self.listCells, self.nmbX, self.nmbY)

		

	def calcule(self):
		self.gen += 1
		for x in range(len(self.listCells)):
			for y in range(len(self.listCells[x])):
				self.listCells[x][y].calcule() #Parcourir chaque cellule et calculer sont état, mort ou vivant

	def calculeVoisine(self):
		for x in range(len(self.listCells)):
			for y in range(len(self.listCells[x])):
				self.listCells[x][y].voisine(self.listCells, self.nmbX, self.nmbY)#Parcourir chaque cellule et calculer ces voisines


	def draw(self, fenetre, pause):
		for x in range(len(self.listCells)):
			for y in range(len(self.listCells[x])):
				self.listCells[x][y].draw(fenetre)

		

pygame.time.set_timer(USEREVENT, 200)

w = World(NMBCASEX,NMBCASEY)
w.init()

pause = True

while True:
	#Les evenements
	#Cas 1, si on a cliqué sur le boutton X
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			break

		#Clavier appuyé
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE: #Touche escape
				pygame.quit()
				break
			if event.key == K_RIGHT: #Touche fleche droite
				w.calcule()
				w.calculeVoisine()
			if event.key == K_p: #Touche p
				if pause == False:
					pause = True
				else:
					pause = False
	
		if event.type == MOUSEBUTTONDOWN:
			mX = event.pos[0]
			mY = event.pos[1]
			if event.button == 1: #clique souris left click

				if 0<=mX<=TAILLECARRE*NMBCASEX and 0<=mY<=TAILLECARRE*NMBCASEY:
					if w.listCells[int(mX/TAILLECARRE)][int(mY/TAILLECARRE)].state == 1:
						w.listCells[int(mX/TAILLECARRE)][int(mY/TAILLECARRE)].state = 0
					else:
						w.listCells[int(mX/TAILLECARRE)][int(mY/TAILLECARRE)].state = 1
					w.calculeVoisine()

		if pause == False:
			if event.type == USEREVENT:
				w.calcule()
				w.calculeVoisine()
	
	w.draw(fenetre, pause)

	#Refresh
	pygame.display.flip()
	clock.tick(FPS)