from queue import PriorityQueue

def es_estado_valido(estado):
    p, l, o, le = estado
    # Si el pastor no está con la oveja...
    if p != o:
        if o == l:
            return False  # El lobo se come la oveja
        if o == le:
            return False  # La oveja se come la lechuga
    return True

def generar_movimientos(estado_str):
    estado = list(estado_str)
    p, l, o, le = estado
    lado_opuesto = 'R' if p == 'L' else 'L'

    movimientos = []

    posibles = [
        ('solo', None),
        ('lobo', 1),
        ('oveja', 2),
        ('lechuga', 3)
    ]

    for tipo, idx in posibles:
        nuevo_estado = estado.copy()
        nuevo_estado[0] = lado_opuesto  # mover pastor

        if idx is not None and estado[idx] == p:
            nuevo_estado[idx] = lado_opuesto

        nuevo_estado_str = "".join(nuevo_estado)
        if es_estado_valido(nuevo_estado):
            movimientos.append(nuevo_estado_str)

    return movimientos

def heuristica(estado, objetivo):
    return sum(1 for i in range(len(estado)) if estado[i] != objetivo[i])

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

# Corregimos el estado inicial (4 letras, no 5)
estado_inicial = "LLLL"
estado_objetivo = "RRRR"

solucion = a_estrella(estado_inicial, estado_objetivo)

# Mostrar solución paso a paso
for i, paso in enumerate(solucion):
    print(f"Paso {i}: P:{paso[0]} L:{paso[1]} O:{paso[2]} LE:{paso[3]}")
