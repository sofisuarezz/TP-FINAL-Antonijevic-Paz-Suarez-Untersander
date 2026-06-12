import pygame
import math
from mapa import *
from main_mapa import *
from setting import (tile_size, vel_pacman_normal, vel_pacman_power,color_pacman,duracion_asustado)

direcciones= {"derecha":(1,0) , "izquierda":(-1,0), "arriba":(0,-1),"abajo":(0,1)}

angulo_base={"derecha":0 , "izquierda":180, "arriba":90,"abajo":270}

tiles_transitables = {" ",".","o","P","T","-"}

class pacman:
    def __init__(self,mapa):
        col_inicial, fila_inicial = mapa.obtener_posicion_pacman()

        self.x= col_inicial*tile_size+tile_size/2
        self.y = fila_inicial *tile_size + tile_size/2

        self.inicial_x = self.x
        self.inicial_y = self.y

        self.direccion = "derecha"
        self.prox_direccion = "derecha"

        self.power_activo = False
        self.comio_power_pellet = False
        self.tiempo_power = 0.0

        self.apertura = 45.0
        self.boca_abriendo = False
        self.vel_boca = 300.0

        self.radio = (tile_size//2) -1

        self.vivo = True
    
    def col (self) -> int:
        return int(self.x)// tile_size
    
    def fila(self)-> int:
        return int(self.y)// tile_size
    
    
    def velocidad(self)->float:
        if self.power_activo:
            return vel_pacman_power
        return vel_pacman_normal
    
    
    def manejar_evento(self,evento):
        if evento.type!= pygame.KEYDOWN:
            return
        teclas= {
                pygame.K_RIGHT: "derecha", 
                pygame.K_LEFT: "izquierda",
                pygame.K_UP: "arriba",
                pygame.K_DOWN:"abajo"
                }
        if evento.key in teclas:
            self.prox_direccion = teclas[evento.key]
    
    def es_transitable(self,col,fila,mapa): 
        try:
            tile =mapa.obtener_tile(col,fila)
        except IndexError:
            return False
        return tile in tiles_transitables
    
    def centrado(self, margen =4): 
        cx_tile = self.col() * tile_size + tile_size / 2
        cy_tile = self.fila() * tile_size + tile_size / 2
        return abs(self.x - cx_tile) <= margen and abs(self.y - cy_tile) <= margen
    
    def alinear_al_tile(self):
        self.x = self.col() *  tile_size + tile_size / 2
        self.y = self.fila() * tile_size + tile_size / 2
    
    def intentar_cambiar_direccion(self, mapa):
        if self.prox_direccion == self.direccion:
            return
        dc, df = direcciones[self.prox_direccion]
        if self.centrado() and self.es_transitable(self.col() + dc,self.fila() + df , mapa):
            self.direccion = self.prox_direccion
            self.alinear_al_tile()
    

    def mover(self, dt, mapa):
        dc, df = direcciones[self.direccion]
        pixels = self.velocidad() * dt

        nuevo_x = self.x + dc * pixels
        nuevo_y = self.y + df * pixels

        col_futuro  = int(nuevo_x + dc * self.radio) // tile_size
        fila_futuro = int(nuevo_y + df * self.radio) // tile_size

        if self.es_transitable(col_futuro, fila_futuro, mapa):
            self.x = nuevo_x
            self.y = nuevo_y
        else:
            self.alinear_al_tile()
    
    def verificar_tunel(self, mapa):
        if mapa.obtener_tile(self.col(), self.fila()) != "T":
            return
    
        if self.col() <= 0:
            self.x = (ancho_mapa - 2) * tile_size + tile_size / 2
        elif self.col() >= ancho_mapa - 1:
            self.x = tile_size + tile_size / 2
            

    def consumir_tile(self, mapa):
        tile = mapa.obtener_tile(self.col(),self.fila() )
        if tile == ".":
            mapa.cambiar_tile(self.col(), self.fila(), " ")
            return 10
        if tile == "o":
            mapa.cambiar_tile(self.col(),self.fila() , " ")
            self.activar_power()
            self.comio_power_pellet = True
            return 50
        return 0

    def activar_power(self):
        self.power_activo  = True
        self.tiempo_power = 0.0

    def actualizar_power(self, dt):
        if not self.power_activo:
            return
        self.tiempo_power += dt
        if self.tiempo_power >= duracion_asustado:
            self.power_activo  = False
            self.tiempo_power = 0.0
    
    def animar_boca(self, dt):
        if self.boca_abriendo:
            self.apertura += self.vel_boca * dt
            if self.apertura >= 45:
                self.apertura = 45
                self.boca_abriendo = False
        else:
            self.apertura -= self.vel_boca * dt
            if self.apertura <= 0:
                self.apertura = 0
                self.boca_abriendo = True
    
    def actualizar(self, dt, mapa):
        if not self.vivo:
            return 0

        self.comio_power_pellet = False
        self.actualizar_power(dt)
        self.intentar_cambiar_direccion(mapa)
        self.mover(dt, mapa)
        self.animar_boca(dt)

        puntos = self.consumir_tile(mapa)
        self.verificar_tunel(mapa)

        return puntos
    
    def colisiona_con(self, fantasma):
        dist = math.hypot(self.x - fantasma.x, self.y - fantasma.y)
        return dist < tile_size * 0.75

    def morir(self):
        self.vivo = False

    def resetear(self):
        self.x              = self.inicial_x
        self.y              = self.inicial_y
        self.direccion      = "derecha"
        self.prox_direccion = "derecha"
        self.power_activo   = False
        self.tiempo_power  = 0.0
        self.apertura      = 45.0
        self.boca_abriendo = False
        self.vivo           = True
    
    def dibujar(self, superficie, offset_y=0):
        cx = int(self.x)
        cy = int(self.y) + offset_y

        pygame.draw.circle(superficie, color_pacman, (cx, cy), self.radio)

        if self.apertura > 0:
            abertura = int(self.apertura / 45 * self.radio)  
            if self.direccion == "derecha":
                puntos = [(cx, cy), (cx + self.radio, cy - abertura), (cx + self.radio, cy + abertura)]
            elif self.direccion == "izquierda":
                puntos = [(cx, cy), (cx - self.radio, cy - abertura), (cx - self.radio, cy + abertura)]
            elif self.direccion == "arriba":
                puntos = [(cx, cy), (cx - abertura, cy - self.radio), (cx + abertura, cy - self.radio)]
            elif self.direccion == "abajo":
                puntos = [(cx, cy), (cx - abertura, cy + self.radio), (cx + abertura, cy + self.radio)]

            pygame.draw.polygon(superficie, (0, 0, 0), puntos)