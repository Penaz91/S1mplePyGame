#!/usr/bin/env python
#--------------------
# Primitive Shooter
# Un semplice shooter in Pygame
#--------------------
# By Penaz
#--------------------

#--------------------
# Imports
#--------------------
import pygame
from pygame import *
from sys import exit
from random import randint
import Vector
from math import floor, ceil
from Vector import *
#--------------------
# Variabili
#--------------------
render_list=pygame.sprite.Group()   #Lista di sprite da disegnare
score=0     #Punteggio
empower=False   #Bool per l'attivazione dei cheat
tp=0    #Tempo
kills=0     #Uccisioni (per le vite bonus)
killlevel=0     #Livello di uccisioni per ottenere una vita bonus
lv=1        #Numero livello
empow=0     #Variabile incrementabile per il controllo dei cheat
shlvl=1     #Livello di potenza del cannone
lives=3     #Vite
pow_list=pygame.sprite.Group()  #Lista di sprite da considerare powerups
enemy_list=pygame.sprite.Group()    #Lista di sprite da considerare nemici
bullets=pygame.sprite.Group()       #Lista dei proiettili su schermo
#--------------------------------------------------
# Classe Giocatore
# Variabili: move_x, move_y per il movimento orizzontale/verticale
#--------------------------------------------------
class Player(pygame.sprite.Sprite):
	move_x=0
	move_y=0
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)     #Inizializzo la superclasse
		self.image=pygame.Surface((20,20))      #Assegno come immagine un quadrato 20x20 px
		self.image.fill((255,255,255))          #Rendo bianco il quadrato
		self.rect=self.image.get_rect()         #Ricavo il rettangolo per le collisioni
		self.rect.x=x                           #Posiziono orizzontalmente la sprite
		self.rect.y=y                           #Posiziono verticalmente la sprite
		render_list.add(self)                   #Aggiungo alla lista di rendering
	def update(self):
		if self.rect.x+self.move_x < 620 and self.rect.x+self.move_x >0:    #Se il movimento orizzontale non provoca un'uscita dallo schermo
			self.rect.x+=self.move_x    #Muoviti
		if self.rect.y+self.move_y < 460 and self.rect.y+self.move_y >0:    #Se il movimento verticale non provoca un'uscita dallo schermo
			self.rect.y+=self.move_y    #Muoviti
		collision=pygame.sprite.spritecollide(self,enemy_list,True)         #Verifico eventuali collisioni tra giocatore e nemici
		if collision:       #Se si verifica una collisione
			global lives
			lives-=1    #Tolgo una vita
#--------------------------------------------------
# Classe PowerUp
#--------------------------------------------------
class Powerup(pygame.sprite.Sprite):
	def __init__(self,x,y):     #È simile a quello della classe player
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((15,15))      #Il quadrato è di 15x15px
		self.image.fill((73,255,234))           #Il colore è azzurro
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		render_list.add(self)
		pow_list.add(self)                      #Aggiungo ai powerups
	def update(self):
		self.rect.y+=2                          #Muoviti costantemente verso il basso
		if self.rect.y>=480:                    #Se esce dallo schermo
			self.kill()                     #Elimina la sprite
		collide=pygame.sprite.spritecollide(player,pow_list,True)   #Verifico la collisione col giocatore
		if collide:     #Se si verifica la collisione
			global shlvl
			shlvl+=1    #Alzo la potenza del cannone
			self.kill() #Elimino la sprite
#--------------------------------------------------
# Classe Nemico
#--------------------------------------------------
class Enemy(pygame.sprite.Sprite):
	destination=0   #La x di destinazione finale
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((20,20))      #È un quadrato 20x20px
		self.image.fill((255,0,0))              #È rosso
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		enemy_list.add(self)                    #Aggiungo alla lista dei nemici
		render_list.add(self)
		self.destination=randint(0,620)         #La x di destinazione è un numero a caso tra 0 e 620 pixel
	def update(self):
		self.rect.y+=3                          #Scendi costantemente
		if self.rect.y>=0:                      #Quando entra nello schermo
			if self.rect.x>self.destination:        #Se sono troppo a destra
				self.rect.x-=randint(1,5)       #Correggo in modo pseudocasuale
			elif self.rect.x < self.destination:    #Se sono troppo a sinistra
				self.rect.x+=randint(1,5)       #Correggo in modo pseudocasuale
			if self.rect.y>480:                     #Se Esco dallo schermo
				self.kill()                     #Elimina la sprite
class PowerBullet(pygame.sprite.Sprite):
	speed=10
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((4,10))
		self.image.fill((17,128,255))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		bullets.add(self)
		render_list.add(self)
	def update(self):
		self.rect.y-=self.speed
		if self.rect.y<=-5:
			self.kill()
		collide=pygame.sprite.spritecollide(self,enemy_list,True)
		if collide:
			global score
			global kills
			score+=20
			kills+=1
			n=randint(0,2)
			if n==1:
				Powerup(320,0)
				global score
				score+=10

class Bullet(pygame.sprite.Sprite):
	speed=300
	direction=Vector()
	heading=Vector()
	move_x=0
	def __init__(self,x,y,dirx):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((2,5))
		self.image.fill((255,128,12))
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		bullets.add(self)
		render_list.add(self)
		self.direction=Vector.FromPoints((x,y),(x+dirx,-20))
		self.direction.normalize()
		self.move_x=(tp/1000.)*self.speed*self.direction.to_tuple()[0]
		if self.move_x<0:
			self.move_x=floor(self.move_x)
		elif self.move_x>0:
			self.move_x=ceil(self.move_x)
	def update(self):
		self.rect.x+=self.move_x
		self.rect.y+=(tp/1000.)*self.speed*self.direction.to_tuple()[1]
		if self.rect.y<=-5:
			self.kill()
		collide=pygame.sprite.spritecollide(self,enemy_list,True)
		if collide:
			self.kill()
			global score
			score+=20
			global kills
			kills+=1
			n=randint(0,15)
			if n==1:
				Powerup(320,0)
				global score
				score+=10
def Shoot():
	if shlvl==1:
		Bullet(player.rect.x+(player.rect.width/2),player.rect.y,0)
	elif shlvl==2:
		Bullet(player.rect.x,player.rect.y,0)
		Bullet(player.rect.x+player.rect.width,player.rect.y,0)
	elif shlvl==3:
		Bullet(player.rect.x+(player.rect.width/2),player.rect.y-10,0)
		Bullet(player.rect.x,player.rect.y,0)
		Bullet(player.rect.x+player.rect.width,player.rect.y,0)
	elif shlvl==4:
		Bullet(player.rect.x+(player.rect.width/2),player.rect.y-10,0)
		Bullet(player.rect.x,player.rect.y,-5)
		Bullet(player.rect.x+player.rect.width,player.rect.y,5)
	elif shlvl==5:
		Bullet(player.rect.x+(3*player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x,player.rect.y,-5)
		Bullet(player.rect.x+(player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x+player.rect.width,player.rect.y,5)
	elif shlvl==6:
		Bullet(player.rect.x+(3*player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x,player.rect.y,-5)
		Bullet(player.rect.x,player.rect.y+10,-7)
		Bullet(player.rect.x+player.rect.width,player.rect.y+10,7)
		Bullet(player.rect.x+(player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x+player.rect.width,player.rect.y,5)
	elif shlvl==7:
		Bullet(player.rect.x+(3*player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x,player.rect.y,-5)
		Bullet(player.rect.x+(player.rect.width/4),player.rect.y-10,0)
		Bullet(player.rect.x+player.rect.width,player.rect.y,5)
		Bullet(player.rect.x,player.rect.y+5,-200)
		Bullet(player.rect.x+player.rect.width,player.rect.y+5,200)
	elif shlvl>7:
		global shlvl
		shlvl=7
player=Player(320,440)
pygame.init()
screen=pygame.display.set_mode((640,480),0,32)
pygame.display.set_caption("Primitive Shooter!!")
clock=pygame.time.Clock()
f=pygame.font.SysFont("Arial",12)
g=pygame.font.SysFont("Arial",30,True,True)
gtext=g.render("Game Over",True,(255,0,0),None)
def Level():
		global killlevel
		killlevel=lv*20
		for n in range(20*lv):
			x=randint(0,640)
			y=randint(-5000,-100)
			Enemy(x,y)
Level()
while True:
	for event in pygame.event.get():
		if event.type==QUIT:
			exit()
		if event.type==KEYDOWN:
			if event.key==K_LEFT:
				player.move_x=-7
			if event.key==K_RIGHT:
				player.move_x=7
			if event.key==K_UP:
				player.move_y=-7
			if event.key==K_DOWN:
				player.move_y=7
			if event.key==K_z:
				if not empower:
					Shoot()
				else:
					PowerBullet(player.rect.x+(player.rect.width/2),player.rect.y)
		if event.type==KEYUP:
			if event.key==K_LEFT:
				player.move_x=0
			if event.key==K_RIGHT:
				player.move_x=0
			if event.key==K_UP:
				player.move_y=0
			if event.key==K_DOWN:
				player.move_y=0
			if event.key==K_e:
				empow=1
			if event.key==K_m and empow==1:
				empow=2
			if event.key==K_p and empow==2:
				empow=3
			if event.key==K_o and empow==3:
				empow=4
			if event.key==K_w and empow==4:
				empower=True
				player.image.fill((255,12,128))
	player.update()
	for bullet in bullets:
		bullet.update()
	screen.fill((0,0,0))
	render_list.draw(screen)
	s=f.render(str(score),True,(255,255,255),None)
	l=f.render("Level "+str(lv),True,(255,255,255),None)
	live=f.render("Lives: " +str(lives),True,(255,255,255),None)
	screen.blit(live,(400,460))
	screen.blit(l,(400,10))
	screen.blit(s,(10,10))
	for enemy in enemy_list:
		enemy.update()
	global kills
	for powerup in pow_list:
		powerup.update()
	if kills==killlevel:
		score+=1000
		lv+=1
		kills=0
		Level()
	if lives<=0:
		player.kill()
		for enemy in enemy_list:
			enemy.kill()
		screen.blit(gtext,(240,200))
	pygame.display.flip()
	global tp
	tp=clock.tick(60)
