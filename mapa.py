from setting import tile_size, map_col, map_filas
caracteres_validos = {"X", "o", ".", " ", "G", "T", "-", "P"}

ancho_mapa = map_col
alto_mapa = map_filas

class Mapa:
    def __init__(self, ruta):
        self.grilla = []
        self.cargar(ruta)
        self.validar()

    def cargar(self, ruta):
        archivo = open(ruta, "r")
        lineas = archivo.read().splitlines()
        archivo.close()

        for linea in lineas:
            fila = list(linea)
            self.grilla.append(fila)

    def validar(self):
        self.validar_dimensiones()
        self.validar_caracteres()
        self.validar_pacman()
        self.validar_ghost_house()

    def validar_dimensiones(self):
        cantidad_filas = len(self.grilla)

        if cantidad_filas != alto_mapa:
            raise ValueError("El mapa debe tener 31 filas")

        for fila in self.grilla:
            if len(fila) != ancho_mapa:
                raise ValueError("Todas las filas deben tener 28 columnas")

    def validar_caracteres(self):
        for fila in self.grilla:
            for caracter in fila:
                if caracter not in caracteres_validos:
                    raise ValueError("El mapa tiene un caracter inválido")

    def validar_pacman(self):
        cantidad_pacman = 0

        for fila in self.grilla:
            for caracter in fila:
                if caracter == "P":
                    cantidad_pacman = cantidad_pacman + 1

        if cantidad_pacman == 0:
            raise ValueError("El mapa no contiene Pac-Man")

        if cantidad_pacman > 1:
            raise ValueError("El mapa tiene más de un Pac-Man")

    def validar_ghost_house(self):
        tiene_g = False
        tiene_puerta = False

        for fila in self.grilla:
            for caracter in fila:
                if caracter == "G":
                    tiene_g = True

                if caracter == "-":
                    tiene_puerta = True

        if tiene_g == False:
            raise ValueError("El mapa no contiene ghost house")

        if tiene_puerta == False:
            raise ValueError("El mapa no contiene puerta de ghost house")

    def is_wall(self, tile):
        columna, fila = tile

        if fila < 0 or fila >= alto_mapa:
            return True

        if columna < 0 or columna >= ancho_mapa:
            return True
        return self.grilla[fila][columna] == "X"

    def es_pared(self, tile):
        return self.is_wall(tile)

    def es_tunel(self, tile_x, tile_y):
        if tile_y < 0 or tile_y >= alto_mapa:
            return False

        if tile_x < 0 or tile_x >= ancho_mapa:
            return False
        return self.grilla[tile_y][tile_x] == "T"

    def teletransportar(self, tile_x, tile_y, pixel_x, pixel_y):
        if tile_x < 0:
            tile_x = ancho_mapa - 1
            pixel_x = tile_x * tile_size

        elif tile_x >= ancho_mapa:
            tile_x = 0
            pixel_x = 0
        return tile_x, tile_y, pixel_x, pixel_y

    def obtener_power_pellets(self):
        pellets = []
        for fila in range(alto_mapa):
            for col in range(ancho_mapa):
                if self.grilla[fila][col] == "o":
                    pellets.append((col, fila))
        return pellets

    def obtener_posicion_pacman(self):
        for fila in range(alto_mapa):
            for col in range(ancho_mapa):
                if self.grilla[fila][col] == "P":
                    return col, fila

    def obtener_tile(self, col, fila):
        return self.grilla[fila][col]

    def cambiar_tile(self, col, fila, caracter):
        if caracter not in caracteres_validos:
            raise ValueError("Caracter inválido")

        self.grilla[fila][col] = caracter

