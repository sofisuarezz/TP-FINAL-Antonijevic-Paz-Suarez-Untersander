import pygame
from mapa import Mapa, ancho_mapa, alto_mapa, tile_size
from pacman import pacman
from ver_mapa import dibujar_mapa, dibujar_texto, dibujar_vidas, margen_superior, margen_inferior
from fantasmas.ghost import *
from fantasmas.personalidades import *


from setting import fps, vidas_iniciales, color_fondo, color_pacman, color_infojuego
from high_score import cargar_high_score,guardar_high_score
from pantalla_gameover import pantalla_game_over


def dibujar_texto_juego(pantalla, fuente, score, high_score):
    texto_1up = fuente.render("1UP", True, color_infojuego)
    texto_score = fuente.render(str(score), True, color_infojuego)

    texto_high = fuente.render("HIGH SCORE", True, color_infojuego)
    texto_high_score = fuente.render(str(high_score), True, color_infojuego)

    pantalla.blit(texto_1up, (70, 10))
    pantalla.blit(texto_score, (85, 35))

    pantalla.blit(texto_high, (220, 10))
    pantalla.blit(texto_high_score, (285, 35))


def dibujar_vidas_juego(pantalla, vidas):
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
    for fila in mapa.grilla:
        for caracter in fila:
            if caracter == "." or caracter == "o":
                return True
    return False

def resetear_posiciones(jugador, fantasmas):
    jugador.resetear()
    for fantasma in fantasmas:
        fantasma.resetear()

pygame.init()

mapa = Mapa("mapa.txt")

ancho_ventana = ancho_mapa * tile_size
alto_ventana  = alto_mapa  * tile_size + margen_superior + margen_inferior

pantalla = pygame.display.set_mode((ancho_ventana, alto_ventana))
pygame.display.set_caption("Pac-Man")

fuente = pygame.font.SysFont("arial", 24, True)
reloj  = pygame.time.Clock()

jugador = pacman(mapa)

blinky_nuevo = Blinky(mapa)
fantasmas = [
    blinky_nuevo,
    Pinky(mapa),
    Inky(mapa, blinky_nuevo),
    Clyde(mapa),
    Facu(mapa),
    Picky(mapa)
]

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

        score += jugador.actualizar(dt, mapa)

        if score > high_score:
            high_score = score
            guardar_high_score(high_score) 



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
            vidas = vidas - 1

            if vidas <= 0:
                resultado = pantalla_game_over(pantalla, score)

                if resultado == "salir":
                    ventana_abierta = False

                if resultado == "reiniciar":
                    mapa = Mapa("mapa.txt")

                    jugador = pacman(mapa)
                    blinky_nuevo = Blinky(mapa)
                    fantasmas = [
                        blinky_nuevo,
                        Pinky(mapa),
                        Inky(mapa, blinky_nuevo),
                        Clyde(mapa),
                        Facu(mapa),
                        Picky(mapa)]

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
            fantasmas = [
                        blinky_nuevo,
                        Pinky(mapa),
                        Inky(mapa, blinky_nuevo),
                        Clyde(mapa),
                        Facu(mapa),
                        Picky(mapa)]
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