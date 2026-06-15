import pygame
from setting import color_fondo, color_pacman, color_infojuego, fps
from high_score import actualizar_high_score


def pantalla_game_over(pantalla: pygame.Surface, score: int) -> str:
    """
    Muestra la pantalla de Game Over cuando el jugador pierde todas sus vidas.

    Actualiza el high score si el puntaje actual lo supera y espera a que
    el jugador decida si quiere reiniciar la partida o salir del juego.

    Argumentos:
        pantalla (pygame.Surface): Ventana principal donde se dibuja la pantalla.
        score (int): Puntaje final obtenido en la partida.

    Retorna:
        str: "reiniciar" si el jugador presiona R, o "salir" si presiona ESC
        o cierra la ventana.
    """
    high_score: int = actualizar_high_score(score)

    reloj: pygame.time.Clock = pygame.time.Clock()

    fuente_titulo: pygame.font.Font = pygame.font.SysFont("arial", 60, True)
    fuente_mediana: pygame.font.Font = pygame.font.SysFont("arial", 32, True)
    fuente_chica: pygame.font.Font = pygame.font.SysFont("arial", 24, True)

    pantalla_abierta: bool = True

    while pantalla_abierta:
        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                return "salir"

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "reiniciar"

                if evento.key == pygame.K_ESCAPE:
                    return "salir"

        pantalla.fill(color_fondo)

        texto_game_over = fuente_titulo.render("GAME OVER", True, color_pacman)
        rect_game_over = texto_game_over.get_rect()
        rect_game_over.center = (pantalla.get_width() // 2, 180)
        pantalla.blit(texto_game_over, rect_game_over)

        texto_score = fuente_mediana.render("SCORE: " + str(score), True, color_infojuego)
        rect_score = texto_score.get_rect()
        rect_score.center = (pantalla.get_width() // 2, 290)
        pantalla.blit(texto_score, rect_score)

        texto_high_score = fuente_mediana.render("HIGH SCORE: " + str(high_score), True, color_infojuego)
        rect_high_score = texto_high_score.get_rect()
        rect_high_score.center = (pantalla.get_width() // 2, 340)
        pantalla.blit(texto_high_score, rect_high_score)

        texto_reiniciar = fuente_chica.render("Presiona R para reiniciar", True, color_infojuego)
        rect_reiniciar = texto_reiniciar.get_rect()
        rect_reiniciar.center = (pantalla.get_width() // 2, 450)
        pantalla.blit(texto_reiniciar, rect_reiniciar)

        texto_salir = fuente_chica.render("Presiona ESC para salir", True, color_infojuego)
        rect_salir = texto_salir.get_rect()
        rect_salir.center = (pantalla.get_width() // 2, 490)
        pantalla.blit(texto_salir, rect_salir)

        pygame.display.flip()
        reloj.tick(fps)