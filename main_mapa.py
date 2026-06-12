from mapa import Mapa

mapa = Mapa("mapa.txt")

print("Mapa cargado correctamente")
print("Pac-Man está en:", mapa.obtener_posicion_pacman())
print("Power pellets:", mapa.obtener_power_pellets())
print("¿La posición 0,0 es pared?", mapa.is_wall((0, 0)))

