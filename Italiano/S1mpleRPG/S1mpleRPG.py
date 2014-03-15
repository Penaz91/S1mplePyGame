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
    move_x=0
    move_y=0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,20))
        self.image.fill((255,255,255))
        self.rect=self.image.get_rect()
        self.rect.x=20
        self.rect.y=20
        todraw.add(self)
    def update(self):
        self.rect.x+=self.move_x
        xcoll()
        self.rect.y+=self.move_y
        ycoll()
        screen.blit(self.image, (self.rect.x, self.rect.y))
def xcoll():
    collision=pygame.sprite.spritecollide(player, plats, False)
    for block in collision:
        if player.move_x>0:
            player.rect.right=block.rect.left
        if player.move_x<0:
            player.rect.left=block.rect.right
def ycoll():
        collision=pygame.sprite.spritecollide(player, plats, False)
        for block in collision:
            if player.move_y<0:
                player.rect.top=block.rect.bottom
            if player.move_y>0:
                player.rect.bottom=block.rect.top
def build():
    myx=0
    global level
    level=[]
    myy=0
    with open("comp","rb") as lvl:
        level=pickle.loads(zlib.decompress(lvl.readline()))
    for r in level:
        for c in r:
            if c==' ':
                pass
            elif c=='#':
                p=Platform(myx,myy)
            myx+=20
        myy+=20
        myx=0
player=Player()
build()
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        if event.type==KEYDOWN:
            if event.key==K_UP:
                    player.move_y=-5
            if event.key==K_LEFT:
                player.move_x=-5
            if event.key==K_RIGHT:
                player.move_x=5
            if event.key==K_DOWN:
                player.move_y=5
        if event.type==KEYUP:
            if event.key==K_LEFT:
                player.move_x=0
            if event.key==K_RIGHT:
                player.move_x=0
            if event.key==K_UP:
                player.move_y=0
            if event.key==K_DOWN:
                player.move_y=0
    todraw.update()
    plats.update()
    pygame.display.update()
    clock.tick(30)
