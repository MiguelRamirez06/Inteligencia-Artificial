from queue import PriorityQueue

def generar_movimientos(estado):
    """
    Genera los posibles movimientos desde un estado dado.
    """
    movimientos = []
    espacio = estado.index("_")

    # Movimiento de una posición (hacia la derecha o izquierda según la rana)
    if espacio > 0 and estado[espacio - 1] == "R":
        nuevo_estado = list(estado)
        nuevo_estado[espacio], nuevo_estado[espacio - 1] = nuevo_estado[espacio - 1], nuevo_estado[espacio]
        movimientos.append("".join(nuevo_estado))

    if espacio < len(estado) - 1 and estado[espacio + 1] == "A":
        nuevo_estado = list(estado)
        nuevo_estado[espacio], nuevo_estado[espacio + 1] = nuevo_estado[espacio + 1], nuevo_estado[espacio]
        movimientos.append("".join(nuevo_estado))

    # Salto sobre una rana
    if espacio > 1 and estado[espacio - 2] == "R" and estado[espacio - 1] != "_":
        nuevo_estado = list(estado)
        nuevo_estado[espacio], nuevo_estado[espacio - 2] = nuevo_estado[espacio - 2], nuevo_estado[espacio]
        movimientos.append("".join(nuevo_estado))

    if espacio < len(estado) - 2 and estado[espacio + 2] == "A" and estado[espacio + 1] != "_":
        nuevo_estado = list(estado)
        nuevo_estado[espacio], nuevo_estado[espacio + 2] = nuevo_estado[espacio + 2], nuevo_estado[espacio]
        movimientos.append("".join(nuevo_estado))

    return movimientos


def heuristica(estado, objetivo):
    """
    Calcula la heurística como la cantidad de ranas fuera de su posición final.
    """
    return sum(1 for i in range(len(estado)) if estado[i] != objetivo[i] and estado[i] != "_")


def a_estrella(inicial, objetivo):
    """
    Algoritmo A* para encontrar la solución más corta.
    """
    cola = PriorityQueue()
    cola.put((0, inicial, [inicial]))  # (costo total, estado actual, camino)
    visitados = set()

    while not cola.empty():
        costo, estado, camino = cola.get()

        if estado == objetivo:
            return camino

        if estado in visitados:
            continue
        visitados.add(estado)

        for nuevo_estado in generar_movimientos(estado):
            if nuevo_estado not in visitados:
                g_n = len(camino)  # Costo real (número de movimientos)
                h_n = heuristica(nuevo_estado, objetivo)  # Estimación de distancia al objetivo
                f_n = g_n + h_n  # Función de evaluación f(n) = g(n) + h(n)
                cola.put((f_n, nuevo_estado, camino + [nuevo_estado]))

    return []


# Estado inicial y objetivo
estado_inicial = "RRR_AAA"
estado_objetivo = "AAA_RRR"

# Ejecutar A* para encontrar la solución
solucion = a_estrella(estado_inicial, estado_objetivo)

# Imprimir el árbol de movimientos
for i, estado in enumerate(solucion):
    print(f"Paso {i}: {estado}")
