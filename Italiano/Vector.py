#--------------------------------------------------
# Vector
# By Penaz
#--------------------------------------------------
import math
class Vector(object):
    """Classe di supporto personalizzata per il calcolo fra vettori"""
    def __init__(self,x=0.,y=0.):
        """Inizializzazione del vettore"""
        self.x=x
        self.y=y
    @staticmethod
    def FromPoints(a,b):
        """Ricava un vettore dati 2 punti"""
        return Vector(b[0]-a[0],b[1]-a[1])
    def __add__ (self,vec2):
        """Somma tra vettori"""
        return Vector(self.x + vec2.x, self.y+vec2.y)
    def __str__(self):
        """Conversione a String"""
        return "(%s,%s)"%(self.x,self.y)
    def __sub__(self,vec2):
        """Sottrazione fra vettori"""
        return Vector(self.x-vec2.x, self.y-vec2.y)
    def __mul__(self,scal):
        """Prodotto per uno scalare"""
        return Vector(self.x*scal, self.y*scal)
    def __div__(self, scal):
        """Divisione per uno scalare"""
        return Vector(self.x/scal, self.y/scal)
    def mod(self):
        """Modulo di un vettore"""
        return float(math.sqrt(self.scalar(self)))
    def __neg__(self):
        """Negazione"""
        return (-self.x, -self.y)
    def scalar(self,vec2):
        """Prodotto scalare di due vettori"""
        return (self.x*vec2.x+self.y*vec2.y)
    def normalize(self):
        """Normalizzazione di un vettore"""
        mod=self.mod()
        if mod==0:
            mod=1
        self.x/=mod
        self.y/=mod
        return
    def to_tuple(self):
        """Conversione a Tuple"""
        return (self.x,self.y)
    def int(self):
        """Arrotondamento delle grandezze caratteristiche del vettore"""
        return (round(self.x),round(self.y))
