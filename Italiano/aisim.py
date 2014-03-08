#!/usr/bin/env python2
#--------------------------------------------------
# S1mpleAiSim
# Una semplice implementazione di intelligenza arificiale
# By Penaz
#--------------------------------------------------
S_S=(640,480)   #Dimensione della finestra
#--------------------------------------------------
# Imports
#--------------------------------------------------
import pygame
from pygame.locals import *
from random import randint, choice
from gameobjects.vector2 import Vector2     #Usate easy_install gameobjects per installare il pacchetto
#--------------------------------------------------
# Classe Stato
# Usata come superclasse di tutti gli stati, nel caso fossero necessarie
# operazioni comuni
#--------------------------------------------------
class state(object):
	def __init__(self,name):
		self.name=name      #Dò un nome allo stato
	def do_action(self):
		pass
	def check_conditions(self):
		pass
	def entry_actions(self):
		pass
	def exit_actions(self):
		pass
#--------------------------------------------------
# Classe Macchina a Stati finiti
# Implemento il "cervello" della IA
#--------------------------------------------------
class StateMachine(object):
	def __init__(self):
		self.states={}      #Stati
		self.active_state=None      #Stato attualmente attivo
        #--------------------
        # Nuovo stato
        #--------------------
	def add_state(self,state):
		self.states[state.name]=state   #Aggiungo lo stato all'elenco degli stati possibili
        #--------------------
        # Diamo alla macchina la capacità di "pensare"
        #--------------------
	def think(self):
		if self.active_state is None:   #Se nessuno stato è attualmente attivo
			return          #non fare nulla
		self.active_state.do_action()       #Altrimenti esegui l'azione richiesta dallo stato attivo
		new_state_name=self.active_state.check_conditions()     #Controlla le condizioni per il cambio di stato
		if new_state_name is not None:      #Se le condizioni sono adatte ad un cambio di stato
			self.set_state(new_state_name)      #Effettua il cambio di stato
        #--------------------
        # Funzione per il cambio di stato
        #--------------------
	def set_state(self,new_state_name):
		if self.active_state is not None:       #Se lo stato attivo non è vuoto
			self.active_state.entry_actions()   #Eseguo le azioni di ingresso nello stato
		self.active_state=self.states[new_state_name]       #prelevo dall'elenco degli stati il nuovo stato impostato
		self.active_state.entry_actions()       #Eseguo le azioni di ingresso nel nuovo stato
#--------------------------------------------------
# Classe "Mondo"
#--------------------------------------------------
class World(object):
	def __init__(self):
		self.entities={}            #Entità presenti
		self.entity_id=0            #Prossimo ID
		self.background=pygame.surface.Surface(S_S).convert()   #Sfondo del mondo
		self.background.fill((255,255,255))                 #Coloro di bianco
        #--------------------
        # Nuova entità
        #--------------------
	def add_entity(self,entity):
		self.entities[self.entity_id]=entity        #Aggiunta dell'entità alla lista
		entity_id=self.entity_id                    #Setto l'id
		self.entity_id+=1                           #Preparo il prossimo ID
        #--------------------
        # Rimuovi entità
        #--------------------
	def rem_entity(self,entity):
		del self.entities[entity.id]        #Semplice eliminazione dalla lista, l'id non viene salvato per praticità
        #--------------------
        # Ricava entità dall'ID
        #--------------------
	def get(self,entity_id):
		if entity_id in self.entities:          #Se l'id esiste
			return self.entities[entity_id]     #Ritornalo
		else:
			return None                 #Altrimenti non ritornare nulla
	def process(self,t_pass):
		tps=t_pass/1000.
		for entity in self.entities.values():
			entity.process(tps)
	def render(self,surface):
		surface.blit(self.background,(0,0))
		for entity in self.entities.itervalues():
			entity.render(surface)
	def get_close_entity(self, name, location, range=200.):
		location=Vector2(*location)
		for entity in self.entities.itervalues():
			if entity.name==name:
				distance = location.get_distance_to(entity.location)
				if distance < range:
					return entity
		return None
class GameEntity(object):
	def __init__(self,world,name,image):
		self.world=world
		self.name=name
		self.image=image
		self.location=Vector2(0,0)
		self.destination=Vector2(0,0)
		self.speed=0.
		self.brain=StateMachine()
		self.id=0
	def render(self,surface):
		x,y=self.location
		w,h=self.image.get_size()
		surface.blit(self.image,(x-w/2,y-h/2))
	def process(self,t_pass):
		try:
			self.brain.think()
		except:
			pass
		if (self.speed > 0.) and (self.location != self.destination):
			vec_to_dest=self.destination-self.location
			dist_to_dest=vec_to_dest.get_length()
			heading=vec_to_dest.get_normalized()
			travel_dist=min(dist_to_dest,t_pass*self.speed)
			self.location+=travel_dist*heading
class Enemy(GameEntity):
	def __init__(self,world,image):
		GameEntity.__init__(self,world,"enemy",image)
		waiting_state=EnemyStateWaiting(self)
		follow_state=EnemyStateFollow(self)
		self.brain.add_state(waiting_state)
		self.brain.add_state(follow_state)
		self.location=Vector2(50,50)
	def render(self,surface):
		GameEntity.render(self,surface)
class EnemyStateWaiting(state):
	def __init__(self,enemy):
		state.__init__(self,"waiting")
		self.enemy=enemy
	def check_conditions(self):
		player=self.enemy.world.get_close_entity("player", self.enemy.location)
		if player is not None:
			self.enemy.player_id=player.id
			return "following"
		return None
class EnemyStateFollow(state):
	def __init__(self,enemy):
		state.__init__(self,"following")
		self.enemy=enemy
		self.player_id=None
	def check_conditions(self):
		player=self.enemy.world.get_close_entity("player", self.enemy.location)
		if player is None:
			self.enemy.destination=self.enemy.location
			return "waiting"
		else:
			self.enemy.destination=player.location
class Player(GameEntity):
	def __init__(self,world,image):
		GameEntity.__init__(self,world,"player",image)
		self.destination=(320,240)
def run():
	pygame.init()
	screen=pygame.display.set_mode(S_S,0,32)
	global world
	world=World()
	w,h=S_S
	clock=pygame.time.Clock()
	player_image=pygame.image.load("player.png").convert_alpha()
	enemy_image=pygame.image.load("enemy.png").convert_alpha()
	enemy=Enemy(world,enemy_image)
	enemy.location=Vector2(randint(0,w),randint(0,h))
	enemy.destination=enemy.location
	enemy.brain.set_state("waiting")
	enemy.speed=5.
	world.add_entity(enemy)
	player=Player(world, player_image)
	player.location=Vector2(320,240)
	player.speed=20.
	world.add_entity(player)
	m_x,m_y=0,0
	t_pass=clock.tick(30)
	mov=(t_pass/1000.)*player.speed
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				quit()
			if event.type==KEYDOWN:
				if event.key == K_s:
					m_y=mov
				if event.key == K_a:
					m_x=-mov
				if event.key == K_w:
					m_y=-mov
				if event.key == K_d:
					m_x=mov
			if event.type==KEYUP:
				if event.key==K_s:
					m_y=0
				if event.key==K_a:
					m_x=0
				if event.key==K_d:
					m_x=0
				if event.key==K_w:
					m_y=0
		player.destination=player.location+Vector2(m_x,m_y)
		world.process(t_pass)
		world.render(screen)
		pygame.display.update()
if __name__ == "__main__":
	run()
