#!/usr/bin/env python3
#--------------------------------------------------
# S1mpleRPG
# Un semplice gioco in stile simil-RPG privo di scorrimento
# Il gioco è una modifica di S1mplePlatformer quindi i nomi delle classi
# potrebbero non rispecchiare il loro significato
# By Penaz
#--------------------------------------------------
#--------------------------------------------------
# Imports
#--------------------------------------------------
import pygame
from pygame.locals import *
from sys import exit
import pickle,zlib
#--------------------------------------------------
# Inizializzazioni e variabili principali
#--------------------------------------------------
pygame.init()       #Avvio moduli Pygame
screen=pygame.display.set_mode((1000,480),0,32)         #Creazione della superficie della finestra
pygame.display.set_caption("S1mpleRPG")           #Settaggio del titolo della finestra
clock=pygame.time.Clock()                       #Clock di sistema per evitare differenze prestazionali
todraw=pygame.sprite.Group()                    #Gruppo delle sprites da disegnare
plats=pygame.sprite.Group()                     #Gruppo delle sprites da considerare muri
#--------------------
# Classe Mura - ex classe platform
#--------------------
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)         #Inizializzazione della superclasse
        self.image=pygame.Surface((20,20))          #L'immagine è un quadrato 20x20 pixel
        self.image.fill((255,0,0))                  #Colore rosso
        self.rect=self.image.get_rect()             #Ricavo il rettangolo per le collisioni
        self.rect.x=x                       #Posizionamento orizzontale
        self.rect.y=y                       #Posizionamento Verticale
        plats.add(self)                     #aggiunta all'elenco dei muri
    def update(self):                   #Aggiornamento dello stato
        screen.blit(self.image, (self.rect.x, self.rect.y))     #Stampa su schermo
#--------------------
# Classe giocatore
#--------------------
class Player(pygame.sprite.Sprite):
    move_x=0            #Movimento orizzontale
    move_y=0            #Movimento Verticale
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)     #Inizializzazione superclasse
        self.image=pygame.Surface((20,20))      #L'immagine è un quadrato 20x20 Pixel
        self.image.fill((255,255,255))          #Riempimento bianco
        self.rect=self.image.get_rect()         #Ricavo il rect per le collisioni
        self.rect.x=20                          #Posizionamento orizzontale
        self.rect.y=20                          #Posizionamento verticale
        todraw.add(self)                        #Aggiungo alle sprites da mostrare a schermo
    #--------------------
    # Aggiornamento dello stato
    #--------------------
    def update(self):
        self.rect.x+=self.move_x                #Movimento orizzontale
        xcoll()                                 #Verifica collisioni sull'asse orizzontale
        self.rect.y+=self.move_y                #Movimento verticale
        ycoll()                                 #Verifica collisioni sull'asse verticale
        screen.blit(self.image, (self.rect.x, self.rect.y))         #Stampa su schermo
#--------------------
# Verifica collisioni sull'asse orizzontale
#--------------------
def xcoll():
    collision=pygame.sprite.spritecollide(player, plats, False)     #Verifica eventuale collisione
    for block in collision:             #Per ogni collisione verificatasi
        if player.move_x>0:                 #Se il giocatore si muoveva verso destra
            player.rect.right=block.rect.left           #Lato destro giocatore=lato sinistro blocco con cui si ha la collisione
        if player.move_x<0:                 #Similmente per il movimento verso sinistra
            player.rect.left=block.rect.right       #...
#--------------------
# Verifica collisioni sull'asse verticale
# Si comporta esattamente come xcoll() ma per i movimenti verticali
#--------------------
def ycoll():
        collision=pygame.sprite.spritecollide(player, plats, False)
        for block in collision:
            if player.move_y<0:
                player.rect.top=block.rect.bottom
            if player.move_y>0:
                player.rect.bottom=block.rect.top
#--------------------
# Routine di costruzione del livello
# Vedi il file level
#--------------------
def build():
    myx=0       #Movimento orizzontale della costruzione
    global level        #Globalizzo level
    level=[]            #Questa variabile contiene lo schema del livello
    myy=0       #Movimento orizzontale della costruzione
    with open("comp","rb") as lvl:      #Apro il file compresso contenente il livello
        level=pickle.loads(zlib.decompress(lvl.readline()))     #Uso pickle e zlib per decomprimere e caricare lo schema del livello
    for r in level:         #Per ogni riga dello schema
        for c in r:         #Per ogni carattere della riga
            if c==' ':      #Se è uno spazio
                pass        #Non inserire nulla
            elif c=='#':        #Altrimenti, se trovi un #
                p=Platform(myx,myy)     #Inserisci un muro in quel punto
            myx+=20         #Spostati a destra di 20 pixel (La dimensione orizzontale di un muro)
        myy+=20         #Spostati in basso di 20 pixel (La dimensione verticale di un muro)
        myx=0           #Resetta myx per la prossima riga
player=Player()     #Nuova istanza del giocatore
build()         #Costruisci il livello
#--------------------
# Ciclo di gioco
#--------------------
while True:
    screen.fill((0,0,0))        #Riempio di nero per evitare scie
    for event in pygame.event.get():        #Ciclo di elaborazione degli eventi
        if event.type==QUIT:        #richiesta di uscita
            exit()          #Esci
        if event.type==KEYDOWN:     #Pressione di un pulsante
            if event.key==K_UP:         #Freccia Su
                    player.move_y=-5        #Movimento verso l'alto di 5px alla volta
            if event.key==K_LEFT:           #Similmente per sinistra, destra e giù
                player.move_x=-5            #...
            if event.key==K_RIGHT:          #...
                player.move_x=5             #...
            if event.key==K_DOWN:           #...
                player.move_y=5             #...
        if event.type==KEYUP:           #Rilascio di un tasto
            if event.key==K_LEFT:       #Freccia sinistra
                player.move_x=0         #Ferma il movimento orizzontale
            if event.key==K_RIGHT:      #Similmente per freccia destra, su, giù
                player.move_x=0         #...
            if event.key==K_UP:         #...
                player.move_y=0         #...
            if event.key==K_DOWN:       #...
                player.move_y=0         #...
    todraw.update()         #Aggiorna tutti gli elementi da disegnare
    plats.update()          #Aggiorna lo stato di tutte le pareti
    pygame.display.update()     #Aggiornamento schermo
    clock.tick(30)              #Tick del clock di sistema
