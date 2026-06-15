import pygame
import setting


class Sonido:
    """
    Clase encargada de cargar y reproducir los sonidos del juego.

    Carga los efectos de sonido de comer puntos, perder una vida
    y el jingle de inicio usando las rutas definidas en setting.py.
    """
    def __init__(self):
        """
        Hace iniciar el sistema de sonido de pygame y carga los archivos de audio.

        También configura el volumen de cada sonido según los valores
        definidos en setting.py.
        """
        pygame.mixer.init()

        self.comer_punto = pygame.mixer.Sound(setting.sonido_comer_punto)
        self.perder_vida = pygame.mixer.Sound(setting.sonido_perder_vida)
        self.jingle_inicio = pygame.mixer.Sound(setting.sonido_jingle_inicio)

        self.comer_punto.set_volume(setting.volumen_sonidos)
        self.perder_vida.set_volume(setting.volumen_sonidos)
        self.jingle_inicio.set_volume(setting.volumen_musica)

    def reproducir_comer_punto(self):
        """
        Reproduce el sonido que se escucha cuando Pac-Man come un punto.
        """
        self.comer_punto.play()

    def reproducir_perder_vida(self):
        """
        Reproduce el sonido que se escucha cuando Pac-Man pierde una vida.
        """
        self.perder_vida.play()

    def reproducir_jingle_inicio(self):
        """
        Reproduce el jingle de inicio del juego.
        """
        self.jingle_inicio.play()
