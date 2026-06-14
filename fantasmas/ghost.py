import pygame
from setting import *
import random

ESTADO_NORMAL = "normal"
ESTADO_ASUSTADO = "asustado"
ESTADO_OJOS = "ojos"
ESTADO_SALIENDO = "saliendo"
ESTADO_ESPERANDO = "esperando"

TIEMPOS_MODO = [
    ("scatter", 7),
    ("chase", 20),
    ("scatter", 7),
    ("chase", 20),
    ("scatter", 5),
    ("chase", 20),
    ("scatter", 5),
    ("chase", 999999),
]

class Ghost:

    def __init__(self, mapa, color, esquina_col, esquina_fila, offset_x = 0):


        col, fila = mapa.obtener_posicion_fantasma()

        self.x = col * tile_size + tile_size / 2 + offset_x
        self.y = fila * tile_size + tile_size / 2

        self.inicial_x = self.x
        self.inicial_y = self.y

        self.esquina_col = esquina_col
        self.esquina_fila = esquina_fila

        self.direccion = "izquierda"

        self.velocidad = vel_fantasma_normal

        self.estado = ESTADO_ESPERANDO
        self.puntos_para_salir = 0

        self.modo= "scatter"
        self.tiempo_modo = 0
        self.indice_modo= 0

        self.tiempo_asustado = 0
        self.ultimo_tile_asustado = None
        self.ultimo_tile_decision = None

        self.sprite_asustado_azul = pygame.transform.scale(
            pygame.image.load("imagenes/blue_asustado.png").convert_alpha(),
            (tile_size * 2, tile_size * 2))

        self.sprite_asustado_blanco = pygame.transform.scale(
            pygame.image.load("imagenes/white_asustado.png").convert_alpha(),
            (tile_size * 2, tile_size * 2))

        self.sprite_ojos = pygame.transform.scale(
            pygame.image.load("imagenes/ojos.png").convert_alpha(),
            (tile_size * 2, tile_size * 2))

        self.sprites = {"derecha": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_derecha.png").convert_alpha(),
                (tile_size * 2, tile_size * 2)),

            "izquierda": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_izquierda.png").convert_alpha(),
                (tile_size * 2, tile_size * 2)),

            "arriba": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_arriba.png").convert_alpha(),
                (tile_size * 2, tile_size * 2)),

            "abajo": pygame.transform.scale(
                pygame.image.load(
                    f"imagenes/{color}_ghost_abajo.png").convert_alpha(),
                (tile_size * 2, tile_size * 2))}


    def col(self):
        return int(self.x) // tile_size

    def fila(self):
        return int(self.y) // tile_size

    def centrado(self, margen=4):

        cx = self.col() * tile_size + tile_size / 2
        cy = self.fila() * tile_size + tile_size / 2

        return (abs(self.x - cx) <= margen and abs(self.y - cy) <= margen)
    
    def alinear_al_tile(self):

        self.x = self.col() * tile_size + tile_size / 2
        self.y = self.fila() * tile_size + tile_size / 2
            
    
    def direcciones_validas(self, mapa):

        validas = []

        for nombre, (dc, df) in direcciones.items():

            col = self.col() + dc
            fila = self.fila() + df

            tile_actual = mapa.obtener_tile(self.col(), self.fila())

            # para teletransportar
            
            if tile_actual == "T" and (col < 0 or col >= map_col):
                validas.append(nombre)
                continue

            if mapa.es_pared((col, fila)):
                continue

            tile = mapa.obtener_tile(col, fila)

            if self.estado != ESTADO_OJOS:
                if tile == "G":
                    continue

                if tile == "-":
                    continue

            validas.append(nombre)

        return validas

    def elegir_direccion(self, mapa, target_col, target_fila):

        direccion_anterior = self.direccion

        opciones = self.direcciones_validas(mapa)

        if len(opciones) == 0:
            return

        direccion_opuesta = opuesta[direccion_anterior]

        # Descarto la dirección de la que viene (como ya tenia antes)
        if direccion_opuesta in opciones and len(opciones) > 1:
            opciones.remove(direccion_opuesta)

        if len(opciones) == 0:
            return

        # Agrego:
        # Si queda una sola opción, no hay una decisión real:
        # el fantasma simplemente sigue por ahí (porque no hay intersección)

        if len(opciones) == 1:

            mejor_direccion = opciones[0]

        else:

            # Si hay más de una opción: intersección
            # y ahí si puede elegir el tile adyacente que minimiza la distancia al target

            mejor_direccion = opciones[0]
            menor_distancia = float("inf")

            for direccion in opciones:

                dc, df = direcciones[direccion]

                nueva_col = self.col() + dc
                nueva_fila = self.fila() + df

                distancia = ((nueva_col - target_col) ** 2 + (nueva_fila - target_fila) ** 2)

                if distancia < menor_distancia:

                    menor_distancia = distancia
                    mejor_direccion = direccion

                elif distancia == menor_distancia and direccion == self.direccion:

                    mejor_direccion = direccion

        if mejor_direccion != self.direccion:
            self.alinear_al_tile()

        self.direccion = mejor_direccion


    def elegir_direccion_asustado(self, mapa):

        opciones = self.direcciones_validas(mapa)

        if len(opciones) == 0:
            return

        direccion_opuesta = opuesta[self.direccion]

        if direccion_opuesta in opciones and len(opciones) > 1:
            opciones.remove(direccion_opuesta)

        self.direccion = random.choice(opciones)

    def get_target_ojos(self):
        col, fila = self.col(), self.fila()
        
        if fila >= 16:
            if col <= 13:
                return (7, 14)   
            else:
                return (22, 14)  
        
        if col == 7 or col == 22:
            if fila > 11:
                return (col, 11)
       
        return (13, 14)

    def asustar(self):

        if self.estado != ESTADO_NORMAL:
            return

        self.estado = ESTADO_ASUSTADO
        self.tiempo_asustado = 0
        self.velocidad = vel_fantasma_asustado

        self.direccion = opuesta[self.direccion] #porque tienen que invertir direccion al cambiar de modo

        #guardo tile donde se asusta para que lo primero sea cmbiar de 
        # direcc y no elegir direccion random denuevo 
        # agregado cuando temblaban 

        self.ultimo_tile_asustado = (self.col(), self.fila())
            

    def morir(self):

        self.estado = ESTADO_OJOS
        self.velocidad = vel_fantasma_ojos
        self.tiempo_asustado = 0

    def actualizar_estado(self, dt):

        if self.estado != ESTADO_ASUSTADO:
            return

        self.tiempo_asustado += dt

        if self.tiempo_asustado >= duracion_asustado:
            self.estado = ESTADO_NORMAL
            self.velocidad = vel_fantasma_normal
            self.tiempo_asustado = 0
            self.ultimo_tile_asustado = None

    def actualizar_modo(self, dt):
        if self.estado != ESTADO_NORMAL:
            return

        nombre_anterior,_= TIEMPOS_MODO[self.indice_modo]
        self.tiempo_modo += dt
        _, duracion = TIEMPOS_MODO[self.indice_modo]

        if self.tiempo_modo >= duracion:
            self.tiempo_modo = 0
            if self.indice_modo < len(TIEMPOS_MODO) - 1:
                self.indice_modo += 1

        nombre_nuevo, _ = TIEMPOS_MODO[self.indice_modo]
        self.modo = nombre_nuevo

        if nombre_nuevo != nombre_anterior:
            self.direccion = opuesta[self.direccion]

    def teletransportar_tunel(self, mapa):

        fila = self.fila()

        if fila < 0 or fila >= map_filas:
            return

        if self.col() < 0:
            if mapa.es_tunel(0, fila):
                self.x = (map_col - 1) * tile_size + tile_size / 2

        elif self.col() >= map_col:
            if mapa.es_tunel(map_col - 1, fila):
                self.x = tile_size / 2

    def mover(self, dt, mapa):

        dc, df = direcciones[self.direccion]

        velocidad = self.velocidad
        
        if mapa.obtener_tile(self.col(), self.fila()) == "T":
            velocidad = vel_fantasma_tunel

        self.x += dc * velocidad * dt
        self.y += df * velocidad * dt

        self.teletransportar_tunel(mapa)

    def actualizar(self, dt, mapa, pacman):

        if self.estado == ESTADO_ESPERANDO:
            return
        self.actualizar_estado(dt)
        self.actualizar_modo(dt)

        if self.estado == ESTADO_SALIENDO:

            puerta_col = 13
            puerta_fila = 12

            puerta_x = puerta_col * tile_size + tile_size / 2
            puerta_y = puerta_fila * tile_size + tile_size / 2

            margen = 2

            # necesito que se alineen horizontalmente con la puerta
            if abs(self.x - puerta_x) > margen:

                if self.x < puerta_x:

                    self.direccion = "derecha"
                    self.x += self.velocidad * dt

                    if self.x > puerta_x:
                        self.x = puerta_x

                else:

                    self.direccion = "izquierda"
                    self.x -= self.velocidad * dt

                    if self.x < puerta_x:
                        self.x = puerta_x

                return

            # ahora si, una vez alineado con la puerta, sube
            if self.y > puerta_y:

                self.x = puerta_x
                self.direccion = "arriba"
                self.y -= self.velocidad * dt

                if self.y < puerta_y:
                    self.y = puerta_y

                return

            self.x = puerta_x
            self.y = puerta_y
            self.estado = ESTADO_NORMAL
            self.direccion = "izquierda"
            self.ultimo_tile_decision = None

            return
        # para que los ojos vuelvan a la ghost house bien 

        if self.estado == ESTADO_OJOS:

            if self.col() == 13 and self.fila() == 14:

                self.estado = ESTADO_SALIENDO
                self.velocidad = vel_fantasma_normal
                self.tiempo_asustado = 0
                self.direccion = "arriba"

                return

        if self.centrado():
            if self.estado == ESTADO_ASUSTADO:
                tile_actual = (self.col(), self.fila())

                # para que solo decida una vez por tile y no titile 
                # (no elija random direc antes de cambiar de direc 
                # porque esta en centrado tdavia)

                if tile_actual != self.ultimo_tile_asustado:

                    self.ultimo_tile_asustado = tile_actual

                    direccion_anterior = self.direccion

                    self.elegir_direccion_asustado(mapa)

                    if self.direccion != direccion_anterior:
                        self.alinear_al_tile()

            else:

                tile_actual = (self.col(), self.fila())

                # Hago que decida una sola vez por tile/intersección
                # porque tengo que evitar que vuelva a recalcular mientras sigue centrado
                # en el mismo tile!

                if tile_actual != self.ultimo_tile_decision:

                    self.ultimo_tile_decision = tile_actual

                    if self.estado == ESTADO_OJOS:
                        target_col, target_fila = self.get_target_ojos()

                    elif self.modo == "scatter":
                        target_col = self.esquina_col
                        target_fila = self.esquina_fila

                    else:
                        target_col, target_fila = self.get_target(pacman)

                    direccion_anterior = self.direccion

                    self.elegir_direccion(mapa, target_col, target_fila)

                    if self.direccion != direccion_anterior:
                        self.alinear_al_tile()

        self.mover(dt,mapa)

    def resetear(self):

        self.x = self.inicial_x
        self.y = self.inicial_y

        self.estado = ESTADO_ESPERANDO

        self.velocidad = vel_fantasma_normal

        self.direccion = "izquierda"

        self.tiempo_asustado = 0

        self.modo = "scatter"

        self.tiempo_modo = 0
        
        self.indice_modo = 0

        self.ultimo_tile_asustado = None

        self.ultimo_tile_decision = None

    def dibujar(self, pantalla, offset_y=0):

        sprite = self.sprites[self.direccion]

        if self.estado == ESTADO_ASUSTADO:

            tiempo_restante = (duracion_asustado - self.tiempo_asustado)
                
            if tiempo_restante <= duracion_parpadeo:

                if int(self.tiempo_asustado * 8) % 2 == 0:
                    sprite = self.sprite_asustado_azul
                else:
                    sprite = self.sprite_asustado_blanco

            else:
                sprite = self.sprite_asustado_azul

        elif self.estado == ESTADO_OJOS:
            sprite = self.sprite_ojos

        offset_x = 0
        offset_y_sprite = 0

        if self.direccion == "arriba":
            offset_x = 1

        elif self.direccion == "abajo":
            offset_x = -1

        elif self.direccion == "izquierda":
            offset_y_sprite = 2

        pantalla.blit(sprite,
            (self.x - sprite.get_width() / 2 + offset_x,
                self.y - sprite.get_height() / 2 + offset_y + offset_y_sprite))