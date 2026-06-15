def cargar_high_score() -> int:
    """
    Lee el high score guardado en el archivo high_score.txt.

    Retorna:
        int: El puntaje máximo guardado.
    """
    archivo = open("high_score.txt", "r")
    contenido = archivo.read()
    archivo.close()

    high_score = int(contenido)

    return high_score


def guardar_high_score(high_score: int) -> None:
    """
    Guarda un nuevo high score en el archivo high_score.txt.

    Argumentos:
        high_score (int): Puntaje máximo que se quiere guardar.
    """
    archivo = open("high_score.txt", "w")
    archivo.write(str(high_score))
    archivo.close()


def actualizar_high_score(score: int) -> int:
    """
    Compara el puntaje actual con el high score guardado.
    Si el puntaje actual es mayor, actualiza el archivo.

    Argumentos:
        score (int): Puntaje obtenido en la partida actual.

    Retorna:
        int: El high score actualizado o el high score anterior.
    """
    high_score = cargar_high_score()

    if score > high_score:
        high_score = score
        guardar_high_score(high_score)

    return high_score