import pygame

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)

# Configuración de la cuadrícula
FILAS = 10

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.texto = None

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

        texto = self.texto

        # Dibuja el texto en el nodo
        if texto is not None:
            fuente = pygame.font.SysFont("Arial", int(self.ancho / 5))
            palabras = texto.split("-")
            y = self.y
            # Ajusta el tamaño de la fuente según el ancho del nodo
            for i in range(len(palabras)):
                superficie_texto = fuente.render(palabras[i], True, (0, 0, 0))
                ventana.blit(superficie_texto, (self.x, y))
                y += int(self.ancho / 5) + 5
            # Dibuja el símbolo "👌" cuando el nodo es visitado
            if self.es_visitado() or self.es_fin() or self.es_inicio() or self.color == VERDE:
                superficie_texto = fuente.render("👌", True, (0, 0, 0))
                ventana.blit(superficie_texto, ((self.x + self.ancho) - int(self.ancho / 5),
                                                (y - int(self.ancho / 5) - 5) if FILAS > 11 else y))

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

# Función para determinar la heurística (distancia de Manhattan)
def heuristica(actually_nodo, objetivo):
    dist_fila = abs(objetivo.get_pos()[0] - actually_nodo.get_pos()[0])
    dist_col = abs(objetivo.get_pos()[1] - actually_nodo.get_pos()[1])
    return (dist_fila + dist_col) * 10

# Función principal para reconstruir el camino
def a_estrella(inicio, final, grid, ventana):
    print("Iniciando A*")

def main(ventana, ancho):
    FILAS = 10
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            # Iniciar el algoritmo A* al presionar la barra espaciadora
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if inicio and fin:
                        a_estrella(inicio, fin, grid, ventana)

            if pygame.mouse.get_pressed()[0]:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Clic derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)