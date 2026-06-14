from fantasmas.ghost import Ghost
import random
from setting import *

class Blinky(Ghost):

    def __init__(self, mapa):

        super().__init__(mapa, "red", esquina_col=25, esquina_fila=1, offset_x=0)

    def get_target(self, pacman):

         return (pacman.col(), pacman.fila())


class Pinky(Ghost):

    def __init__(self, mapa):
        super().__init__(mapa, "pink", esquina_col=2, esquina_fila=0, offset_x= tile_size)

    def get_target(self, pacman):
        
        if pacman.direccion == "arriba" :
            return ( pacman.col() -4, pacman.fila() -4)

        dc, df = direcciones[pacman.direccion]

        target_col  = pacman.col()  + dc * 4
        target_fila = pacman.fila() + df * 4

        return target_col, target_fila
    

class Inky(Ghost): 

    def __init__(self, mapa, blinky=None, otros_fantasmas=None):

        super().__init__(mapa, "blue", esquina_col=25, esquina_fila=29, offset_x=-tile_size)

        self.blinky = blinky

        if otros_fantasmas is None:
            self.otros_fantasmas = []
        else:
            self.otros_fantasmas = otros_fantasmas

        self.fantasma_referencia_azar = None

    def obtener_fantasma_referencia(self):

        if self.blinky is not None:
            return self.blinky

        if self.fantasma_referencia_azar is not None:
            return self.fantasma_referencia_azar

        candidatos = []

        for fantasma in self.otros_fantasmas:

            if fantasma is not self:
                candidatos.append(fantasma)

        if len(candidatos) == 0:
            raise ValueError(
                "Inky necesita a Blinky o al menos otro fantasma como referencia"
            )

        self.fantasma_referencia_azar = random.choice(candidatos)

        return self.fantasma_referencia_azar

    def get_target(self, pacman):
        
        if pacman.direccion == "arriba":

            punto_x = pacman.col() - 2
            punto_y = pacman.fila() - 2
        
        else:

            dc, df = direcciones[pacman.direccion]

            punto_x = pacman.col() + dc * 2
            punto_y = pacman.fila() + df * 2

        fantasma_referencia = self.obtener_fantasma_referencia()

        vx = punto_x - fantasma_referencia.col()
        vy = punto_y - fantasma_referencia.fila()

        return (punto_x + vx, punto_y + vy)
            

class Clyde(Ghost):

    def __init__(self, mapa):

        super().__init__(mapa, "orange", esquina_col=2, esquina_fila=29, offset_x=tile_size)

    def get_target(self, pacman):

        distancia = ((self.col() - pacman.col()) ** 2 + (self.fila() - pacman.fila()) ** 2)

        if distancia > 64:

            return (pacman.col(),pacman.fila())
                
        return (self.esquina_col, self.esquina_fila)
            
            
class Facu(Ghost):

    def __init__(self, mapa):

        super().__init__(mapa, "green", esquina_col=0, esquina_fila=30, offset_x=-tile_size)

    def get_target(self, pacman):

        distancia = ((self.col() - pacman.col()) ** 2 + (self.fila() - pacman.fila()) ** 2)

        if distancia <= 64:
            return (pacman.col(), pacman.fila())

        return (self.esquina_col, self.esquina_fila)
            
    
class Picky(Ghost):

    def __init__(self, mapa):

        super().__init__(mapa, "purple", esquina_col=2, esquina_fila=29, offset_x=2 * tile_size)
        self.mapa = mapa
        self.pellet_objetivo = None

    def distancia(self, pos1, pos2):

        col1, fila1 = pos1
        col2, fila2 = pos2

        return ((col1 - col2) ** 2 + (fila1 - fila2) ** 2)

    def pellet_mas_cercano_a_pacman(self, pacman):

        pellets = self.mapa.obtener_power_pellets()

        if len(pellets) == 0:
            return None

        pos_pacman = (pacman.col(), pacman.fila())
        mejor_pellet = None
        mejor_distancia = float("inf")

        for pellet in pellets:
            distancia = self.distancia(pos_pacman, pellet)
                
            if distancia < mejor_distancia:
                mejor_distancia = distancia
                mejor_pellet = pellet

        return mejor_pellet

    def actualizar_pellet_objetivo(self, pacman):

        pellets = self.mapa.obtener_power_pellets()

        if len(pellets) == 0:
            self.pellet_objetivo = None
            return

        if self.pellet_objetivo is None:
            self.pellet_objetivo = self.pellet_mas_cercano_a_pacman(pacman)
            return

        if self.pellet_objetivo not in pellets:
            self.pellet_objetivo = self.pellet_mas_cercano_a_pacman(pacman)
            return

        pos_pacman = (pacman.col(), pacman.fila())

        distancia_actual = self.distancia(pos_pacman, self.pellet_objetivo)

        nuevo_pellet = self.pellet_mas_cercano_a_pacman(pacman)

        distancia_nueva = self.distancia(pos_pacman, nuevo_pellet)
            
        if distancia_nueva + 64 < distancia_actual:
            self.pellet_objetivo = nuevo_pellet


    def target_de_guardia(self, pellet):

        col, fila = pellet

        if col < 14 and fila < 15:
            return (6, 5)       # zona arriba izquierda

        if col >= 14 and fila < 15:
            return (21, 5)      # zona arriba derecha

        if col < 14 and fila >= 15:
            return (2, 23)      # zona abajo izquierda

        return (25, 23)         # zona abajo derecha

    def get_target(self, pacman):

        self.actualizar_pellet_objetivo(pacman)

        if self.pellet_objetivo is None:

            return (pacman.col(), pacman.fila())

        pos_pacman = (pacman.col(), pacman.fila())

        distancia_al_pellet = self.distancia(pos_pacman, self.pellet_objetivo)

        if distancia_al_pellet <= 25:
            return (pacman.col(), pacman.fila())

        return self.target_de_guardia(self.pellet_objetivo)

    # Metodo auxiliar 
    # Lo usé para revisar el target real de Picky, sus direcciones válidas y la dirección elegida,
    #  ya que al principio tenía comportamientos raros (cuando apuntaba exactamente al pellet podía 
    # trabarse, por eso se definieron "zonas de guardia" cercanas al pellet en lugar de usar siempre
    # la coordenada exacta del power pellet)

    def debug(self, pacman):

        if self.estado == "asustado":
            target_real = "random asustado"

        elif self.estado == "ojos":
            target_real = (13, 14)

        elif self.estado == "saliendo":
            target_real = "saliendo de casa"

        elif self.modo == "scatter":
            target_real = (self.esquina_col, self.esquina_fila)
            
        else:
            target_real = self.get_target(pacman)

        print(
            "PICKY |",
            "pos:", (self.col(), self.fila()),
            "| pacman:", (pacman.col(), pacman.fila()),
            "| pellet objetivo:", self.pellet_objetivo,
            "| target real:", target_real,
            "| estado:", self.estado,
            "| modo:", self.modo,
            "| dir:", self.direccion,
            "| validas:", self.direcciones_validas(self.mapa)
        )
        
    def resetear(self):

        super().resetear()
        self.pellet_objetivo = None