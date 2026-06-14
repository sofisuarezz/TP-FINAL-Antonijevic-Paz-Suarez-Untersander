import pygame
import sys
from setting import *

pygame.init()
 
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("PAC-MAN")
 

NEGRO        = (0, 0, 0)
AMARILLO     = (255, 255, 0)
BLANCO       = (255, 255, 255)
GRIS         = (150, 150, 150)
GRIS_OSCURO  = (60, 60, 60)
AZUL_OSCURO  = (0, 0, 180)
 

fuente_grande  = pygame.font.SysFont("monospace", 72, bold=True)
fuente_mediana = pygame.font.SysFont("monospace", 32, bold=True)
fuente_chica   = pygame.font.SysFont("monospace", 22)
fuente_mini    = pygame.font.SysFont("monospace", 18)
 

fantasmas_disponibles = [
    {"nombre": "Blinky", "color": (230, 30,  30),  "desc": "El perseguidor. Siempre te sigue."},
    {"nombre": "Pinky",  "color": (255, 180, 220), "desc": "La emboscadora. Te corta el paso."},
    {"nombre": "Inky",   "color": (0,   220, 230), "desc": "El flanqueador. Impredecible."},
    {"nombre": "Clyde",  "color": (230, 140, 0),   "desc": "El timido. Huye si te acercas."},
    {"nombre": "Facu",   "color": (50,  200, 120), "desc": "El perezoso. Persigue si estas cerca."},
    {"nombre": "Picky",  "color": (180, 120, 230), "desc": "La guardiana. Ronda el power pellet"}]
 

nombres_esquinas = [
    "Superior izquierda",
    "Superior derecha",
    "Inferior izquierda",
    "Inferior derecha",
]
 
clock = pygame.time.Clock()
 
 

def dibujar_inicio(tick, high_score):

    pantalla.fill(NEGRO)

    texto_hs = fuente_chica.render("HIGH SCORE", True, BLANCO)
    texto_pts = fuente_mediana.render(str(high_score), True, AMARILLO)

    pantalla.blit(texto_hs, (ancho // 2 - texto_hs.get_width() // 2, 40))
    pantalla.blit(texto_pts, (ancho // 2 - texto_pts.get_width() // 2, 70))

    titulo = fuente_grande.render("PAC-MAN", True, AMARILLO)
    pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 180))

    if (tick // 30) % 2 == 0:
        msg = fuente_mediana.render("Presiona ENTER para jugar", True, BLANCO)
        pantalla.blit(msg, (ancho // 2 - msg.get_width() // 2, 420))
 
 
def dibujar_seleccion(seleccionados):
  
    pantalla.fill(NEGRO)

    fuente_titulo = pygame.font.SysFont("monospace", 30, bold=True)
    fuente_opcion = pygame.font.SysFont("monospace", 27, bold=True)
    fuente_desc = pygame.font.SysFont("monospace", 16)
    fuente_info = pygame.font.SysFont("monospace", 17)

    titulo = fuente_titulo.render("ELEGÍ 4 FANTASMAS", True, AMARILLO)
    pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 18))

    contador = fuente_info.render(f"Elegidos: {len(seleccionados)}/4", True, BLANCO)
    pantalla.blit(contador, (ancho // 2 - contador.get_width() // 2, 58))

    ayuda = fuente_info.render("Presioná 1-6 para elegir", True, GRIS)
    pantalla.blit(ayuda, (ancho // 2 - ayuda.get_width() // 2, 82))

    y_base = 120

    for i, fantasma in enumerate(fantasmas_disponibles):
        y = y_base + i * 70
        elegido = i in seleccionados

        if elegido:
            pygame.draw.rect(pantalla, GRIS_OSCURO, (30, y - 6, ancho - 60, 60), border_radius=8)
            pygame.draw.rect(pantalla, AMARILLO, (30, y - 6, ancho - 60, 60), 2, border_radius=8)

        num_txt = fuente_opcion.render(str(i + 1), True, AMARILLO)
        pantalla.blit(num_txt, (45, y + 8))

        pygame.draw.circle(pantalla, fantasma["color"], (105, y + 22), 20)

        nombre_txt = fuente_opcion.render(fantasma["nombre"], True, fantasma["color"])
        pantalla.blit(nombre_txt, (140, y))

        desc_txt = fuente_desc.render(fantasma["desc"], True, GRIS)
        pantalla.blit(desc_txt, (140, y + 33))

        if elegido:
            check = fuente_opcion.render("✓", True, AMARILLO)
            pantalla.blit(check, (ancho - 65, y + 8))

    if len(seleccionados) == 4:
        msg = fuente_info.render("ENTER para continuar", True, AMARILLO)
    else:
        msg = fuente_info.render("Necesitás elegir exactamente 4", True, GRIS)

    pantalla.blit(msg, (ancho // 2 - msg.get_width() // 2, alto - 32))
 
 
def dibujar_asignacion(fantasmas_elegidos, indice_actual, esquinas_asignadas):
    pantalla.fill(NEGRO)
    fantasma = fantasmas_elegidos[indice_actual]
 
    titulo = fuente_mediana.render("ASIGNÁ UNA ESQUINA", True, AMARILLO)
    pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 25))
 
    prog = fuente_chica.render(
        f"Fantasma {indice_actual + 1} de {len(fantasmas_elegidos)}",
        True, GRIS
    )
    pantalla.blit(prog, (ancho // 2 - prog.get_width() // 2, 70))

    pygame.draw.circle(pantalla, fantasma["color"], (ancho // 2, 170), 38)
 
    nombre_txt = fuente_mediana.render(fantasma["nombre"], True, fantasma["color"])
    pantalla.blit(nombre_txt, (ancho // 2 - nombre_txt.get_width() // 2, 218))
 
    pregunta = fuente_chica.render("¿A qué esquina va este fantasma?", True, BLANCO)
    pantalla.blit(pregunta, (ancho // 2 - pregunta.get_width() // 2, 268))
 
    y_base = 320
    x_rect = 70
    ancho_rect = ancho - 140
    alto_rect = 40
    fuente_opcion_asig = pygame.font.SysFont("monospace", 18, bold=True)
    for i, nombre_esq in enumerate(nombres_esquinas):
        y = y_base + i * 52

        ya_usada = i in esquinas_asignadas.values()
 
        if ya_usada:
            color_txt  = GRIS_OSCURO
            color_num  = GRIS_OSCURO
            fondo_rect = GRIS_OSCURO
        else:
            color_txt  = BLANCO
            color_num  = AMARILLO
            fondo_rect = GRIS_OSCURO
 

        pygame.draw.rect(pantalla, fondo_rect, (x_rect, y, ancho_rect, alto_rect), border_radius=6)
        if not ya_usada:
            pygame.draw.rect(pantalla, AMARILLO, (x_rect, y, ancho_rect, alto_rect), 1, border_radius=6)
 

            num = fuente_opcion_asig.render(str(i + 1), True, color_num)
            pantalla.blit(num, (x_rect + 20, y + 8))
 

        esq_txt = fuente_opcion_asig.render(nombre_esq, True, color_txt)
        pantalla.blit(esq_txt, (x_rect + 65, y + 8))

        if ya_usada:
            for fant_nombre, esq_idx in esquinas_asignadas.items():
                if esq_idx == i:
                    ocupada = fuente_mini.render(f"(Asignada a {fant_nombre})", True, GRIS)

                    rect_ocupada = ocupada.get_rect()
                    rect_ocupada.center = (ancho // 2, y + 20)

                    pantalla.blit(ocupada, rect_ocupada)
    
    volver = fuente_mini.render("BACKSPACE para deshacer la última asignación",True,GRIS)
    pantalla.blit(volver,(ancho // 2 - volver.get_width() // 2, alto - 25))
 
 
def dibujar_resumen(fantasmas_elegidos, esquinas_asignadas):
    
    pantalla.fill(NEGRO)
 
    titulo = fuente_grande.render("LISTOS!", True, AMARILLO)
    pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 30))
 
    subtitulo = fuente_chica.render("Configuración del juego", True, GRIS)
    pantalla.blit(subtitulo, (ancho // 2 - subtitulo.get_width() // 2, 110))
 
    pygame.draw.line(pantalla, AMARILLO, (100, 140), (ancho - 100, 140), 1)
 
    y_base = 165
    for i, fantasma in enumerate(fantasmas_elegidos):
        y = y_base + i * 80
 
        pygame.draw.circle(pantalla, fantasma["color"], (140, y + 22), 22)
 
        nombre_txt = fuente_mediana.render(fantasma["nombre"], True, fantasma["color"])
        pantalla.blit(nombre_txt, (180, y + 4))
 
        esq_idx  = esquinas_asignadas[fantasma["nombre"]]
        esq_nombre = nombres_esquinas[esq_idx]
        flecha   = fuente_chica.render(f"→  {esq_nombre}", True, BLANCO)
        pantalla.blit(flecha, (180, y + 38))
 
    pygame.draw.line(pantalla, AMARILLO, (100, alto - 80), (ancho - 100, alto - 80), 1)
 
    msg = fuente_chica.render("Presiona ENTER para comenzar la partida", True, AMARILLO)
    pantalla.blit(msg, (ancho // 2 - msg.get_width() // 2, alto - 55))

def pantalla_inicio(high_score):
 
    estado = "inicio"         
 
    seleccionados      = []   
    fantasmas_elegidos = []    
    esquinas_asignadas = {}   
    indice_asignacion  = 0     
    tick               = 0     
    while True:
        tick += 1
 
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            if event.type == pygame.KEYDOWN:
 
               
                if estado == "inicio":
                    if event.key == pygame.K_RETURN:
                        estado = "seleccion"
 
               
                elif estado == "seleccion":
                    teclas_num = {
                        pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
                        pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
                    }
                    if event.key in teclas_num:
                        idx = teclas_num[event.key]
                        if idx in seleccionados:
                            seleccionados.remove(idx)       
                        elif len(seleccionados) < 4:
                            seleccionados.append(idx)      
 
                    if event.key == pygame.K_RETURN and len(seleccionados) == 4:
                       
                        fantasmas_elegidos = [fantasmas_disponibles[i] for i in seleccionados]
                        estado = "asignacion"
                        indice_asignacion = 0
 
                elif estado == "asignacion":
                    teclas_esq = {
                        pygame.K_1: 0, pygame.K_2: 1,
                        pygame.K_3: 2, pygame.K_4: 3,
                    }
                    if event.key == pygame.K_BACKSPACE:
                        if indice_asignacion > 0:
                            indice_asignacion -= 1
                            nombre_anterior = fantasmas_elegidos[indice_asignacion]["nombre"]
                            del esquinas_asignadas[nombre_anterior]
                    if event.key in teclas_esq:
                        esq_idx = teclas_esq[event.key]
                        
                        if esq_idx not in esquinas_asignadas.values():
                            nombre_actual = fantasmas_elegidos[indice_asignacion]["nombre"]
                            esquinas_asignadas[nombre_actual] = esq_idx
                            indice_asignacion += 1
                            if indice_asignacion >= len(fantasmas_elegidos):
                                estado = "resumen"
 
                
                elif estado == "resumen":
                    if event.key == pygame.K_RETURN:
                        
                        return fantasmas_elegidos, esquinas_asignadas
 
        
        if estado == "inicio":
            dibujar_inicio(tick, high_score)
 
        elif estado == "seleccion":
            dibujar_seleccion(seleccionados)
 
        elif estado == "asignacion":
            dibujar_asignacion(fantasmas_elegidos, indice_asignacion, esquinas_asignadas)
 
        elif estado == "resumen":
            dibujar_resumen(fantasmas_elegidos, esquinas_asignadas)
 
        pygame.display.flip()
        clock.tick(60)
 
 
if __name__ == "__main__":
    resultado = pantalla_inicio(0) 
 
    fantasmas, esquinas = resultado
 
    print("\n--- Configuración elegida ---")
    for f in fantasmas:
        esq = esquinas[f["nombre"]]
        print(f"  {f['nombre']}  →  {nombres_esquinas[esq]}")
 
    pygame.quit()
    sys.exit()