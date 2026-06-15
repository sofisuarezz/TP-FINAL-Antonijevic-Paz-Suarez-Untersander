import pygame
from mapa import Mapa, ancho_mapa, alto_mapa, tile_size
from pacman import pacman
from ver_mapa import dibujar_mapa,dibujar_texto, dibujar_vidas, margen_superior, margen_inferior
from fantasmas.ghost import *
from fantasmas.personalidades import *
from sonidos import Sonido
from pdeinicio import pantalla_inicio

from setting import  fps,vidas_iniciales, color_fondo, color_pacman, color_infojuego
from high_score import cargar_high_score,guardar_high_score
from pantalla_gameover import pantalla_game_over


def dibujar_texto_juego(pantalla, fuente, score, high_score):
    """
    Dibuja el score actual y el high score 
    """
    texto_1up = fuente.render("1UP", True, color_infojuego)
    texto_score = fuente.render(str(score), True, color_infojuego)

    texto_high = fuente.render("HIGH SCORE", True, color_infojuego)
    texto_high_score = fuente.render(str(high_score), True, color_infojuego)

    pantalla.blit(texto_1up, (70, 10))
    pantalla.blit(texto_score, (85, 35))

    pantalla.blit(texto_high, (220, 10))
    pantalla.blit(texto_high_score, (285, 35))


def dibujar_vidas_juego(pantalla, vidas):
    """
    Dibuja los íconos de vidas restantes
    """
    y = margen_superior + alto_mapa * tile_size + 30

    for i in range(vidas):
        x = 30 + i * 35

        pygame.draw.circle(pantalla, color_pacman, (x, y), 12)

        pygame.draw.polygon(
            pantalla,
            color_fondo,
            [(x, y), (x + 14, y - 7), (x + 14, y + 7)]
        )

def quedan_puntos(mapa):
    """
    Devuelve True si todavía hay puntos o power pellets en el mapa
    """
    for fila in mapa.grilla:
        for caracter in fila:
            if caracter == "." or caracter == "o":
                return True
    return False

def resetear_posiciones(jugador, fantasmas):
    """
    Resetea la posición de Pac-Man y de todos los fantasmas a sus posiciones iniciales
    """
    jugador.resetear()
    for fantasma in fantasmas:
        fantasma.resetear()

def obtener_esquina(indice):
    """
    Devuelve la columna y fila correspondientes a una esquina del mapa según su índice (0 a 3)
    """
    if indice == 0:
        return 2, 0

    if indice == 1:
        return 25, 0

    if indice == 2:
        return 2, 29

    if indice == 3:
        return 25, 29


def crear_fantasmas(fantasmas_elegidos, esquinas_asignadas, mapa):
    """
    Crea y devuelve la lista de fantasmas según los elegidos por el usuario, asignándoles su esquina de scatter
    """
    fantasmas = []

    blinky_referencia = None

    for fantasma in fantasmas_elegidos:
        if fantasma["nombre"] == "Blinky":
            blinky_referencia = Blinky(mapa)

    if blinky_referencia is None:
        blinky_referencia = Blinky(mapa)

    for fantasma in fantasmas_elegidos:
        nombre = fantasma["nombre"]
    
        if nombre == "Blinky":
            nuevo_fantasma = blinky_referencia

        elif nombre == "Pinky":
            nuevo_fantasma = Pinky(mapa)

        elif nombre == "Inky":
            nuevo_fantasma = Inky(mapa, blinky_referencia)

        elif nombre == "Clyde":
            nuevo_fantasma = Clyde(mapa)

        elif nombre == "Facu":
            nuevo_fantasma = Facu(mapa)

        elif nombre == "Picky":
            nuevo_fantasma = Picky(mapa)

        indice_esquina = esquinas_asignadas[nombre]
        esquina_col, esquina_fila = obtener_esquina(indice_esquina)

        nuevo_fantasma.esquina_col = esquina_col
        nuevo_fantasma.esquina_fila = esquina_fila

        fantasmas.append(nuevo_fantasma)

    return fantasmas

pygame.init()

sonido = Sonido()
high_score = cargar_high_score()
sonido.reproducir_jingle_inicio()
fantasmas_elegidos, esquinas_asignadas = pantalla_inicio(high_score)


mapa = Mapa("mapa.txt")

ancho_ventana = ancho_mapa * tile_size
alto_ventana  = alto_mapa  * tile_size + margen_superior + margen_inferior

pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Pac-Man")

fuente = pygame.font.SysFont("arial", 24, True)
reloj  = pygame.time.Clock()

jugador = pacman(mapa)

fantasmas = crear_fantasmas(fantasmas_elegidos, esquinas_asignadas, mapa)

puntos_salida = [0, 30, 60, 90, 90, 90]

for i in range(len(fantasmas)):
    fantasmas[i].puntos_para_salir = puntos_salida[i]

score = 0
high_score = cargar_high_score()
vidas = vidas_iniciales


ventana_abierta = True
pausa_reinicio = 0

while ventana_abierta:
    dt = reloj.tick(60) / 1000.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ventana_abierta = False
        jugador.manejar_evento(evento)

    if pausa_reinicio > 0:
        pausa_reinicio -= dt

    else:

        pacman_comido = False 

        puntos_ganados = jugador.actualizar(dt, mapa)

        if puntos_ganados > 0:
            sonido.reproducir_comer_punto()

        score += puntos_ganados

        if score > high_score:
            high_score = score
            guardar_high_score(high_score) 
        
        for fantasma in fantasmas:
            if fantasma.estado == ESTADO_ESPERANDO and score >= fantasma.puntos_para_salir:
                fantasma.estado = ESTADO_SALIENDO


        if jugador.comio_power_pellet:
            for fantasma in fantasmas:
                fantasma.asustar()

        for fantasma in fantasmas:
            fantasma.actualizar(dt, mapa, jugador)

        pacman_comido = False

        for fantasma in fantasmas:
            if jugador.colisiona_con(fantasma):
                if fantasma.estado == ESTADO_ASUSTADO:
                    fantasma.morir()
                    score = score + 200

                elif fantasma.estado == ESTADO_NORMAL:
                    pacman_comido = True


        if pacman_comido:
            sonido.reproducir_perder_vida()
            vidas = vidas - 1

            if vidas <= 0:
                resultado = pantalla_game_over(pantalla, score)

                if resultado == "salir":
                    ventana_abierta = False

                if resultado == "reiniciar":
                    mapa = Mapa("mapa.txt")

                    jugador = pacman(mapa)
                    blinky_nuevo = Blinky(mapa)
                    fantasmas = crear_fantasmas(fantasmas_elegidos, esquinas_asignadas, mapa)
                    
                    puntos_salida = [0, 30, 60, 90, 90, 90]
                    for i in range(len(fantasmas)):
                        fantasmas[i].puntos_para_salir = puntos_salida[i]

                    score = 0
                    high_score = cargar_high_score()
                    vidas = vidas_iniciales
                    pausa_reinicio = 0

                    
            else:
                resetear_posiciones(jugador, fantasmas)
                pausa_reinicio = 2.0
        
        if not quedan_puntos(mapa):
            mapa = Mapa("mapa.txt")
            jugador = pacman(mapa)
            blinky_nuevo = Blinky(mapa)
            fantasmas = crear_fantasmas(fantasmas_elegidos, esquinas_asignadas, mapa)
            
            puntos_salida = [0, 30, 60, 90, 90, 90]
            for i in range(len(fantasmas)):
                fantasmas[i].puntos_para_salir = puntos_salida[i]
    
            pausa_reinicio = 2.0


    pantalla.fill((0, 0, 0))
    dibujar_texto_juego(pantalla, fuente,score, high_score)
    dibujar_mapa(pantalla, mapa)
    dibujar_vidas_juego(pantalla,vidas)
    jugador.dibujar(pantalla, offset_y=margen_superior)
    
    for fantasma in fantasmas:
        fantasma.dibujar(pantalla, margen_superior)

    pygame.display.flip()

pygame.quit()