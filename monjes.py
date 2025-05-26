from queue import PriorityQueue

def es_estado_valido(m, c):
    return (m == 0 or m >= c) and (3 - m == 0 or (3 - m) >= (3 - c))

def generar_movimientos(estado):
    movimientos = []
    m, c, lado = int(estado[0]), int(estado[1]), estado[2]

    direc = -1 if lado == 'L' else 1  # -1: L -> R, 1: R -> L
    nuevo_lado = 'R' if lado == 'L' else 'L'

    # Posibles movimientos de la lancha (hasta 2 personas)
    opciones = [
        (1, 0), (2, 0),  # 1 o 2 monjes
        (0, 1), (0, 2),  # 1 o 2 caníbales
        (1, 1)           # 1 monje y 1 caníbal
    ]

    for dm, dc in opciones:
        nuevo_m = m + direc * dm
        nuevo_c = c + direc * dc

        # Validar si las cantidades están en rango
        if 0 <= nuevo_m <= 3 and 0 <= nuevo_c <= 3:
            if es_estado_valido(nuevo_m, nuevo_c):
                nuevo_estado = f"{nuevo_m}{nuevo_c}{nuevo_lado}"
                movimientos.append(nuevo_estado)

    return movimientos

def heuristica(estado, objetivo):
    m, c, _ = int(estado[0]), int(estado[1]), estado[2]
    return m + c  # personas que faltan por cruzar

def a_estrella(inicial, objetivo):
    cola = PriorityQueue()
    cola.put((0, inicial, [inicial]))
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
                g_n = len(camino)
                h_n = heuristica(nuevo_estado, objetivo)
                f_n = g_n + h_n
                cola.put((f_n, nuevo_estado, camino + [nuevo_estado]))

    return []

# Estados inicial y objetivo
estado_inicial = "33L"
estado_objetivo = "00R"

# Ejecutar A*
solucion = a_estrella(estado_inicial, estado_objetivo)

# Mostrar solución paso a paso
for i, paso in enumerate(solucion):
    print(f"Paso {i}: Monjes Izq={paso[0]}, Caníbales Izq={paso[1]}, Lancha={paso[2]}")
