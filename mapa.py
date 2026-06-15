from setting import tile_size, map_col, map_filas


caracteres_validos: set[str] = {"X", "o", ".", " ", "G", "T", "-", "P"}

ancho_mapa: int = map_col
alto_mapa: int = map_filas


class Mapa:
    """
    Representa el mapa del Pac-Man.

    Lee el archivo mapa.txt, lo convierte en una grilla y valida
    que tenga los elementos necesarios para que el juego funcione.
    """

    def __init__(self, ruta: str) -> None:
        """
        Crea un mapa a partir de un archivo de texto.

        Argumentos:
            ruta (str): Ruta del archivo que contiene el mapa.
        """
        self.grilla: list[list[str]] = []
        self.cargar(ruta)
        self.validar()

    def cargar(self, ruta: str) -> None:
        """
        Lee el archivo del mapa y lo guarda como una grilla de caracteres.

        Argumentos:
            ruta (str): Ruta del archivo del mapa.
        """
        archivo = open(ruta, "r")
        lineas = archivo.read().splitlines()
        archivo.close()

        for linea in lineas:
            fila = list(linea)
            self.grilla.append(fila)

    def validar(self) -> None:
        """
        Ejecuta todas las validaciones necesarias del mapa.
        """
        self.validar_dimensiones()
        self.validar_caracteres()
        self.validar_pacman()
        self.validar_ghost_house()

    def validar_dimensiones(self) -> None:
        """
        Verifica que el mapa tenga la cantidad correcta de filas y columnas.

        Errores:
            ValueError: Si el mapa no tiene 31 filas o 28 columnas.
        """
        cantidad_filas = len(self.grilla)

        if cantidad_filas != alto_mapa:
            raise ValueError("El mapa debe tener 31 filas")

        for fila in self.grilla:
            if len(fila) != ancho_mapa:
                raise ValueError("Todas las filas deben tener 28 columnas")

    def validar_caracteres(self) -> None:
        """
        Verifica que el mapa solo tenga caracteres válidos.

        Errores:
            ValueError: Si aparece un símbolo que el juego no reconoce.
        """
        for fila in self.grilla:
            for caracter in fila:
                if caracter not in caracteres_validos:
                    raise ValueError("El mapa tiene un caracter inválido")

    def validar_pacman(self) -> None:
        """
        Verifica que exista una única posición inicial para Pac-Man.

        Errores:
            ValueError: Si no hay Pac-Man o si hay más de uno.
        """
        cantidad_pacman = 0

        for fila in self.grilla:
            for caracter in fila:
                if caracter == "P":
                    cantidad_pacman = cantidad_pacman + 1

        if cantidad_pacman == 0:
            raise ValueError("El mapa no contiene Pac-Man")

        if cantidad_pacman > 1:
            raise ValueError("El mapa tiene más de un Pac-Man")

    def validar_ghost_house(self) -> None:
        """
        Verifica que exista la casa de fantasmas y su puerta.

        Errores:
            ValueError: Si falta la casa de fantasmas o su puerta.
        """
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

    def is_wall(self, tile: tuple[int, int]) -> bool:
        """
        Indica si una posición del mapa es una pared.

        Argumentos:
            tile (tuple[int, int]): Posición del mapa en formato columna, fila.

        Retorna:
            bool: True si la posición es una pared o está fuera del mapa.
        """
        columna, fila = tile

        if fila < 0 or fila >= alto_mapa:
            return True

        if columna < 0 or columna >= ancho_mapa:
            return True

        return self.grilla[fila][columna] == "X"

    def es_pared(self, tile: tuple[int, int]) -> bool:
        """
        Indica si una posición es pared.

        Argumentos:
            tile (tuple[int, int]): Posición del mapa en formato columna, fila.

        Retorna:
            bool: True si la posición es una pared.
        """
        return self.is_wall(tile)

    def es_tunel(self, tile_x: int, tile_y: int) -> bool:
        """
        Indica si una posición corresponde a un túnel.

        Argumentos:
            tile_x (int): Columna del mapa.
            tile_y (int): Fila del mapa.

        Retorna:
            bool: True si la posición es un túnel.
        """
        if tile_y < 0 or tile_y >= alto_mapa:
            return False

        if tile_x < 0 or tile_x >= ancho_mapa:
            return False

        return self.grilla[tile_y][tile_x] == "T"

    def teletransportar(
        self,
        tile_x: int,
        tile_y: int,
        pixel_x: float,
        pixel_y: float
    ) -> tuple[int, int, float, float]:
        """
        Teletransporta al personaje cuando atraviesa un túnel lateral.

        Argumentos:
            tile_x (int): Columna actual.
            tile_y (int): Fila actual.
            pixel_x (float): Posición horizontal en píxeles.
            pixel_y (float): Posición vertical en píxeles.

        Retorna:
            tuple[int, int, float, float]: Nueva posición en tiles y píxeles.
        """
        if tile_x < 0:
            tile_x = ancho_mapa - 1
            pixel_x = tile_x * tile_size

        elif tile_x >= ancho_mapa:
            tile_x = 0
            pixel_x = 0

        return tile_x, tile_y, pixel_x, pixel_y

    def obtener_power_pellets(self) -> list[tuple[int, int]]:
        """
        Busca todas las power pellets del mapa.

        Retorna:
            list[tuple[int, int]]: Lista de posiciones donde hay power pellets.
        """
        pellets = []

        for fila in range(alto_mapa):
            for col in range(ancho_mapa):
                if self.grilla[fila][col] == "o":
                    pellets.append((col, fila))

        return pellets

    def obtener_posicion_pacman(self) -> tuple[int, int]:
        """
        Busca la posición inicial de Pac-Man en el mapa.

        Retorna:
            tuple[int, int]: Columna y fila donde está Pac-Man.

        Errores:
            ValueError: Si no se encuentra la posición inicial de Pac-Man.
        """
        for fila in range(alto_mapa):
            for col in range(ancho_mapa):
                if self.grilla[fila][col] == "P":
                    return col, fila

        raise ValueError("No se encontró la posición inicial de Pac-Man")

    def obtener_tile(self, col: int, fila: int) -> str:
        """
        Devuelve el carácter que hay en una posición del mapa.

        Argumentos:
            col (int): Columna del mapa.
            fila (int): Fila del mapa.

        Retorna:
            str: Caracter ubicado en esa posición.
        """
        return self.grilla[fila][col]

    def cambiar_tile(self, col: int, fila: int, caracter: str) -> None:
        """
        Cambia el carácter de una posición del mapa.

        Argumentos:
            col (int): Columna del mapa.
            fila (int): Fila del mapa.
            caracter (str): Nuevo carácter que se quiere colocar.

        Errores:
            ValueError: Si el carácter no es válido.
        """
        if caracter not in caracteres_validos:
            raise ValueError("Caracter inválido")

        self.grilla[fila][col] = caracter

    def obtener_posicion_fantasma(self) -> tuple[int, int]:
        """
        Devuelve una posición inicial para los fantasmas.

        Retorna:
            tuple[int, int]: Columna y fila inicial de los fantasmas.
        """
        return 13, 14