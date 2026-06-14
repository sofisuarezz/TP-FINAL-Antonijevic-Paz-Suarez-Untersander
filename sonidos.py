import pygame
import setting 

class Sonido:
    def __innit__(self):
        pygame.mixer.init()
        self.comer_punto = pygame.mixer.Sound(setting.sonido_comer_punto)
        self.perder_vida = pygame.mixer.Sound(setting.sonido_perder_vida)
        self.jingle_inicio = pygame.mixer.Sound(setting.sonido_jingle_inicio)

        self.comer_punto.set_volume(setting.volumen_sonidos)
        self.perder_vida.set_volume(setting.volumen_sonidos)
        self.jingle_inicio.set_volume(setting.volumen_musica)

    def reproducir_comer_punto(self):
        self.comer_punto.play()

    def reproducir_perder_vida(self):
        self.perder_vida.play()

    def reproducir_jingle_inicio(self):
        self.jingle_inicio.play()

