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
	def do_action(self):            #Esegui azione
		pass
	def check_conditions(self):     #Verifica condizioni
		pass
	def entry_actions(self):        #Azioni di entrata
		pass
	def exit_actions(self):         #Azioni in uscita
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
        #--------------------
        # Processa le varie entità
        #--------------------
	def process(self,t_pass):
		tps=t_pass/1000.            #Calcolo il tempo trascorso in secondi
		for entity in self.entities.values():       #Per ogni entità
			entity.process(tps)             #Processala
        #--------------------
        # Rendering delle entità
        #--------------------
	def render(self,surface):		surface.blit(self.background,(0,0))         #Riempimento dello sfondo, per evitare scie
		for entity in self.entities.itervalues():       #Per ogni entità
			entity.render(surface)                  #Esegui il render sulla superficie indicata
        #--------------------
        # Verifica se un'entità è vicina ad un'altra entità
        #--------------------
	def get_close_entity(self, name, location, range=200.):
		location=Vector2(*location)                     #Salva la location come vettore dato dall'unpacking dell'argomento
		for entity in self.entities.itervalues():           #Per ogni entità
			if entity.name==name:                   #Se il nome dell'entità corrisponde a quello indicato nell'argomento
				distance = location.get_distance_to(entity.location)        #ricavane la distanza
				if distance < range:            #Se l'entità è nel range
					return entity           #Ritornala
		return None                                     #Altrimenti non ritornare nulla
#--------------------------------------------------
# Classe Entità di gioco, usata come superclasse di molte entità
#--------------------------------------------------
class GameEntity(object):
	def __init__(self,world,name,image):
		self.world=world            #Definizione del mondo "in cui sta" l'entità
		self.name=name              #Nome dell'entità
		self.image=image            #Immagine assegnata
		self.location=Vector2(0,0)  #Posizione (sotto forma di vettore)
		self.destination=Vector2(0,0)   #Destinazione dell'entità in movimento (sotto forma di vettore)
		self.speed=0.               #Velocità dell'entità in movimento
		self.brain=StateMachine()   #Il "Cervello" dell'entità, sotto forma di macchina a stati finiti
		self.id=0                   #ID dell'entità
        #--------------------
        # Funzione di Rendering dell'entità
        #--------------------
	def render(self,surface):
		x,y=self.location           #Unpacking della posizione dell'entità
		w,h=self.image.get_size()   #Unpacking delle dimensioni dell'entità
		surface.blit(self.image,(x-w/2,y-h/2))      #Stampa su schermo nella superficie assegnata
        #--------------------
        # Processa le funzioni dell'entità
        #--------------------
	def process(self,t_pass):
		try:                                #Prova a
			self.brain.think()          #Pensare
		except:                             #Altrimenti
			pass                        #Non fare nulla
		if (self.speed > 0.) and (self.location != self.destination):       #Se l'entità è in movimento
			vec_to_dest=self.destination-self.location              #Trova il vettore che conduce alla destinazione
			dist_to_dest=vec_to_dest.get_length()                   #Ricavane la lunghezza
			heading=vec_to_dest.get_normalized()                    #Normalizza il vettore, per avere un vettore direzione
			travel_dist=min(dist_to_dest,t_pass*self.speed)         #Distanza di viaggio
			self.location+=travel_dist*heading                      #Muovi l'entità
#--------------------------------------------------
# Classe Nemico, eredita da GameEntity
#--------------------------------------------------
class Enemy(GameEntity):
	def __init__(self,world,image):
		GameEntity.__init__(self,world,"enemy",image)           #Inizializzazione della superclasse
		waiting_state=EnemyStateWaiting(self)                   #Definisco uno stato "Nemico in attesa"
		follow_state=EnemyStateFollow(self)                     #Definisco uno stato "Inseguimento"
		self.brain.add_state(waiting_state)                     #Aggiungo lo stato al cervello dell'entità
		self.brain.add_state(follow_state)                      #Aggiungo lo stato al cervello dell'entità
		self.location=Vector2(50,50)                            #Definisco la posizione
        #--------------------
        # Funzione di Rendering dell'entità
        #--------------------
	def render(self,surface):
		GameEntity.render(self,surface)                     #Richiamo la funzione della superclasse
#--------------------------------------------------
# Classe Nemico in attesa, eredita da State
#--------------------------------------------------
class EnemyStateWaiting(state):
	def __init__(self,enemy):
		state.__init__(self,"waiting")              #Inizializzazione della superclasse
		self.enemy=enemy                            #Rendo locale l'argomento dato
        #--------------------
        # Verifica delle condizioni per un eventuale cambio di stato
        #--------------------
	def check_conditions(self):
		player=self.enemy.world.get_close_entity("player", self.enemy.location)     #Verifico se il giocatore è vicino al nemico
		if player is not None:          #Se il giocatore è vicino
			self.enemy.player_id=player.id      #Prendo l'ID dell'entità corrispondente
			return "following"          #Attivo lo stato "inseguimento"
		return None
#--------------------------------------------------
# Classe Nemico in inseguimento, eredita da State
#--------------------------------------------------
class EnemyStateFollow(state):
	def __init__(self,enemy):
		state.__init__(self,"following")            #Inizializzazione della superclasse
		self.enemy=enemy                            #Rendo locale l'argomento dato
		self.player_id=None                         #id del giocatore
        #--------------------
        # Verifica delle condizioni per un eventuale cambio di stato
        #--------------------
	def check_conditions(self):
		player=self.enemy.world.get_close_entity("player", self.enemy.location)         #Verifico se il giocatore è vicino al nemico
		if player is None:                  #Se il giocatore è troppo lontano
			self.enemy.destination=self.enemy.location      #Rendo la destinazione del nemico la propria posizione, in pratica lo fermo
			return "waiting"                    #Passo allo stato "in attesa"
		else:               #Altrimenti
			self.enemy.destination=player.location          #La destinazione è la posizione del giocatore, in pratica insegui il giocatore
#--------------------------------------------------
# Classe Giocatore, eredita da GameEntity
#--------------------------------------------------
class Player(GameEntity):
	def __init__(self,world,image):
		GameEntity.__init__(self,world,"player",image)      #Inizializzazione della superclasse
		self.destination=(320,240)          #Imposto la posizione
#--------------------------------------------------
# Ciclo principale del gioco
#--------------------------------------------------
def run():
	pygame.init()           #Avvio dei moduli di pygame
	screen=pygame.display.set_mode(S_S,0,32)        #Settaggio della superficie dello schermo
	global world            #Rendo globale la variabile world
	world=World()           #E vi assegno un instanza di World
	w,h=S_S                 #Altezza e larghezza dello schermo
	clock=pygame.time.Clock()       #Clock di sistema, per evitare differenze di velocità
	player_image=pygame.image.load("player.png").convert_alpha()            #Immagine del giocatore, con gestione della trasparenza
	enemy_image=pygame.image.load("enemy.png").convert_alpha()              #Immagine del nemico, con gestione della trasparenza
	enemy=Enemy(world,enemy_image)                                          #Creo il nemico
	enemy.location=Vector2(randint(0,w),randint(0,h))           #Decido una posizione casuale per il nemico
	enemy.destination=enemy.location                #Evito che il nemico si muova appena creato
	enemy.brain.set_state("waiting")            #Lo stato del nemico è "in attesa"
	enemy.speed=5.              #Velocità predefinita del nemico
	world.add_entity(enemy)         #Aggiungo al mondo l'entità nemico
	player=Player(world, player_image)      #Creo un'istanza della classe giocatore
	player.location=Vector2(320,240)        #Lo posiziono al centro del mondo
	player.speed=20.                    #Velocità del giocatore
	world.add_entity(player)            #Aggiungo al mondo l'entità Giocatore
        m_x,m_y=0,0                         #Inizializzo 2 variabili: m_x m_y per il movimento del giocatore
	t_pass=clock.tick(30)               #Tick dell'orologio, ne tengo conto per conteggiare il tempo passato
	mov=(t_pass/1000.)*player.speed     #Calcolo della velocità di movimento del giocatore, per evitare differenze prestazionali
	while True:             #Ciclo infinito
		for event in pygame.event.get():            #Gestione degli eventi
			if event.type==QUIT:            #Uscita dal gioco
				quit()              #Chiusura
			if event.type==KEYDOWN:             #Pressione di un tasto
				if event.key == K_s:        #Tasto "s"
					m_y=mov             #Movimento verso il basso con velocità mov
				if event.key == K_a:        #Tasto "a"
					m_x=-mov            #Movimento verso sinistra con velocità mov
				if event.key == K_w:        #Tasto "w"
					m_y=-mov            #Movimento verso l'alto con velocità mov
				if event.key == K_d:        #Tasto "d"
					m_x=mov             #Movimento verso destra con velocità mov
			if event.type==KEYUP:           #Rilascio di un tasto
				if event.key==K_s:      #s
					m_y=0           #Blocco movimento verticale
				if event.key==K_a:      #Similmente per i successivi
					m_x=0           #...
				if event.key==K_d:      #...
					m_x=0           #...
				if event.key==K_w:      #...
					m_y=0           #...
		player.destination=player.location+Vector2(m_x,m_y)     #La destinazione dell'oggetto giocatore è data dalla posizione attuale+spostamento
		world.process(t_pass)               #Processa tutte le entità nel mondo
		world.render(screen)                #Esegui il render del mondo sulla superficie "screen"
		pygame.display.update()             #Aggiornamento dello schermo
if __name__ == "__main__":          #Avvio del programma
	run()                       #
