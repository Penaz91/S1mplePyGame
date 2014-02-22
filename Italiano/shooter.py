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
            #Inizializzazione
		pygame.sprite.Sprite.__init__(self)     #Inizializzo la superclasse
		self.image=pygame.Surface((20,20))      #Assegno come immagine un quadrato 20x20 px
		self.image.fill((255,255,255))          #Rendo bianco il quadrato
		self.rect=self.image.get_rect()         #Ricavo il rettangolo per le collisioni
		self.rect.x=x                           #Posiziono orizzontalmente la sprite
		self.rect.y=y                           #Posiziono verticalmente la sprite
		render_list.add(self)                   #Aggiungo alla lista di rendering
	def update(self):
            #Aggiornamento dello stato/schermo
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
				global kills
				kills+=1                    #Aggiungo 1 alle kills
#--------------------------------------------------
# Classe proiettile speciale
#--------------------------------------------------
class PowerBullet(pygame.sprite.Sprite):
	speed=10        #Velocità del proiettile
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((4,10))       #È un rettangolo 4x10px
		self.image.fill((17,128,255))           #È azzurro
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		bullets.add(self)                       #Aggiungo alla lista dei proiettili
		render_list.add(self)
	def update(self):
		self.rect.y-=self.speed                 #Sali costantemente di "speed"
		if self.rect.y<=-5:             #Se Esci dallo schermo
			self.kill()             #Elimina la sprite
		collide=pygame.sprite.spritecollide(self,enemy_list,True)       #Verifico la collisione proiettile/nemico
		if collide:     #Se si verifica la collisione
			global score
			global kills
			score+=20       #Aggiungo 20 punti
			kills+=1        #Aumento le uccisioni
			n=randint(0,2)      #Creo un intero a caso che è 0 o 1
			if n==1:    #Se è 1
				Powerup(320,0)      #Il nemico lascia un powerup
#--------------------------------------------------
# Classe proiettile
#--------------------------------------------------
class Bullet(pygame.sprite.Sprite):
	speed=300       #Velocità proiettile
	direction=Vector()      #Direzione del proiettile
	move_x=0                #Eventuale Movimento orizzontale
	def __init__(self,x,y,dirx):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.Surface((2,5))        #È un rettangolo 2x5px
		self.image.fill((255,128,12))           #Colore arancione
		self.rect=self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		bullets.add(self)
		render_list.add(self)
		self.direction=Vector.FromPoints((x,y),(x+dirx,-20))    #Creo un vettore per la direzione del proiettile
		self.direction.normalize()                              #Normalizzo il vettore, così tutti i proiettili avranno la stessa velocità
		self.move_x=(tp/1000.)*self.speed*self.direction.to_tuple()[0]      #Definisco il movimento orizzontale a seconda della velocità, del tempo dato dal clock di sistema e dalla coordinata orizzontale del vettore
		if self.move_x<0:                           #|
			self.move_x=floor(self.move_x)      #| Questa parte di codice mi permette di muovere i proiettili in modo discreto
		elif self.move_x>0:                         #| evitando problemi dati da eventuali "mezzi pixel"
			self.move_x=ceil(self.move_x)       #|
	def update(self):
		self.rect.x+=self.move_x            #Movimento orizzontale
		self.rect.y+=(tp/1000.)*self.speed*self.direction.to_tuple()[1]     #Movimento verticale definito in modo analogo a quello della riga 152
		if self.rect.y<=-5:         #Se esce dal campo di gioco
			self.kill()         #Elimina la sprite
		collide=pygame.sprite.spritecollide(self,enemy_list,True)   #|
		if collide:                                                 #|
			self.kill()                                         #|
			global score                                        #|
			score+=20                                           #| Gestisco le collisioni in modo simile alla classe PowerBullet
			global kills                                        #| Ma rendo meno probabile lo spawn di powerups
			kills+=1                                            #|
			n=randint(0,15)                                     #|
			if n==1:                                            #|
				Powerup(320,0)                              #|
#--------------------------------------------------
# Classe che gestisce il fuoco dei cannoni
# Per ogni livello produce un certo numero di proiettili
# Con diversi movimenti orizzontali/verticali
# Creando progressivamente una rosa di proiettili sempre più ampia
# Massimo 7 livelli di potenza
#--------------------------------------------------
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
player=Player(320,440)      #Crea un'istanza del giocatore
pygame.init()               #Inizializza Pygame
screen=pygame.display.set_mode((640,480),0,32)      #Crea schermo: 640x480 a 32bit
pygame.display.set_caption("Primitive Shooter!!")   #Titolo della finestra
clock=pygame.time.Clock()                           #Nuovo orologio di sistema, per evitare di avere differenze di velocità a seconda dell'hardware
f=pygame.font.SysFont("Arial",12)                   #Un oggetto testo da 12px
g=pygame.font.SysFont("Arial",30,True,True)         #Un oggetto testo da 30px
gtext=g.render("Game Over",True,(255,0,0),None)     #Preparo il testo di Game Over
#--------------------------------------------------
# Routine per la creazione del livello
#--------------------------------------------------
def Level():
		global killlevel
		killlevel=lv*20             #Numero di uccisioni per terminare il livello
		for n in range(20*lv):
			x=randint(0,640)        #Definisco la posizione orizzontale del nemico
			y=randint(-5000,-100)   #Definisco la posizione verticale (fuori dal campo di gioco) cioè la distanza dal giocatore
			Enemy(x,y)              #Creo il nemico
Level()     #Crea il primo livello
while True:
	for event in pygame.event.get():        #Elabora gli eventi
		if event.type==QUIT:        #Evento di uscita
			exit()              #Esci
		if event.type==KEYDOWN:     #Pressione di un tasto
			if event.key==K_LEFT:   #Freccia sinistra
				player.move_x=-7    #Muovi a sinistra di 7 pixel
			if event.key==K_RIGHT:      #|
				player.move_x=7     #|
			if event.key==K_UP:         #| Similmente per destra,su e giù
				player.move_y=-7    #|
			if event.key==K_DOWN:       #|
				player.move_y=7     #|
			if event.key==K_z:      #Pressione di Z
				if not empower:     #Se non è attivo il cheat
					Shoot()     #Spara normalmente
				else:       #Altrimenti
					PowerBullet(player.rect.x+(player.rect.width/2),player.rect.y)          #Crea un proiettile speciale
		if event.type==KEYUP:               #Rilascio di un tasto
			if event.key==K_LEFT:       #Freccia sinistra
				player.move_x=0     #Blocca il movimento orizzontale
			if event.key==K_RIGHT:      #|
				player.move_x=0     #|
			if event.key==K_UP:         #| Similmente per su, giu e destra
				player.move_y=0     #|
			if event.key==K_DOWN:       #|
				player.move_y=0     #|
			if event.key==K_e:                              #|
				empow=1                                 #|
			if event.key==K_m and empow==1:                 #|
				empow=2                                 #|
			if event.key==K_p and empow==2:                 #|
				empow=3                                 #| Se l'utente scrive "empow" attivo il cheat e coloro
			if event.key==K_o and empow==3:                 #| il giocatore di fucsia
				empow=4                                 #|
			if event.key==K_w and empow==4:                 #|
				empower=True                            #|
				player.image.fill((255,12,128))         #|
	player.update()             #Aggiorna lo stato del giocatore
	for bullet in bullets:      #Per ogni proiettile esistente
		bullet.update()     #Aggiorna
	screen.fill((0,0,0))        #Riempi lo schermo di nero o resteranno delle scie
	render_list.draw(screen)        #Disegna tutta la render_list sullo schermo
	s=f.render(str(score),True,(255,255,255),None)          #Prepara la scritta per il punteggio
	l=f.render("Level "+str(lv),True,(255,255,255),None)    #Prepara la scritta del livello
	live=f.render("Lives: " +str(lives),True,(255,255,255),None)        #Prepara la scritta del numero di vite
	screen.blit(live,(400,460))         #Disegna il numero di vite a 400x460px
	screen.blit(l,(400,10))             #Disegna il numero di livello a 400x10px
	screen.blit(s,(10,10))              #Disegna il punteggio a 10x10px
        ######Nota: L'origine degli assi (0,0) è nell'angolo in alto a sinistra dello schermo######
	for enemy in enemy_list:    #Per ogni nemico esistente
		enemy.update()          #Aggiorna
	global kills
	for powerup in pow_list:        #Per ogni powerup su schermo
		powerup.update()        #Aggiorna
	if kills==killlevel:        #Se raggiungo il limite di uccisioni->Fine livello
		score+=1000         #Aggiungo 1000 ai punti
		lv+=1               #Nuovo livello
		kills=0             #Reset delle kill
		Level()             #Crea livello
	if lives<=0:        #Vite terminate
		player.kill()       #Elimina il giocatore
		for enemy in enemy_list:        #|Elimina tutti i nemici
			enemy.kill()            #|
		screen.blit(gtext,(240,200))    #Scrivi game over su schermo
	pygame.display.flip()       #Disegna lo schermo
	global tp
	tp=clock.tick(60)           #Tick per la velocità di rendering
