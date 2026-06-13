def cargar_high_score():
    archivo = open("high_score.txt", "r")
    contenido = archivo.read()
    archivo.close()

    high_score = int(contenido)

    return high_score


def guardar_high_score(high_score):
    archivo = open("high_score.txt", "w")
    archivo.write(str(high_score))
    archivo.close()


def actualizar_high_score(score):
    high_score = cargar_high_score()

    if score > high_score:
        high_score = score
        guardar_high_score(high_score)

    return high_score