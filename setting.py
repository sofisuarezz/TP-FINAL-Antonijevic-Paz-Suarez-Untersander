
tile_size= 24
map_col = 28
map_filas= 31


ancho = tile_size * map_col
alto = tile_size* map_filas + 60

fps = 60


vel_max = 7.5 *tile_size
vel_pacman_normal = vel_max * 0.80
vel_pacman_power = vel_max * 0.90
vel_fantasma_normal = vel_max * 0.75
vel_fantasma_asustado = vel_max * 0.50
vel_fantasma_tunel = vel_max * 0.40
vel_fantasma_ojos = vel_max * 1.50

direcciones = {"derecha": (1, 0), "izquierda": (-1, 0), "arriba": (0, -1), "abajo": (0, 1)}
opuesta = {"derecha": "izquierda", "izquierda": "derecha", "arriba": "abajo", "abajo": "arriba"}

duracion_asustado = 6.0
duracion_parpadeo= 2.0


vidas_iniciales= 3
punto_dot=10
puntos_power_pellet= 50


color_fondo= (0,0,0)
color_pared =(28,42,237)
color_dot = (255,255,255)
color_power_pellet = (255, 255, 255)
color_ghost_house = (80, 80, 80)
color_puerta = (255, 150, 255)
color_tunel = (30, 30, 30)
color_texto=(255,255,255)
color_pacman=  (255,255,0)
color_infojuego = (255,255,255)
