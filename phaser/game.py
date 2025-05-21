import pygame
import random
import csv
from datetime import datetime
import os
import pandas as pd

directory_to_save_datasets = 'C:/Users/migue/PycharmProjects/InteligenciaArtificial/phaser/datasets'
directory_to_save_desition_tree = 'C:/Users/migue/PycharmProjects/InteligenciaArtificial/phaser/desition_tree'
decision_tree_trained = None
modo_decision_tree = False

# Variables para el modelo de regresión lineal
linear_regression_model = None
directory_to_save_linear_regression = 'C:/Users/migue/PycharmProjects/InteligenciaArtificial/phaser/linear_regression'

directory_to_save_neural_network = 'C:/Users/migue/PycharmProjects/InteligenciaArtificial/phaser/neural_network'
neural_network_trained = None
mode_neural_network = False
prediction_counter = 0

last_csv_path_saved_for_horizontal_ball = ''
last_csv_path_saved_for_vertical_ball = ''

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
w, h = 1000, 600
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Variables del jugador, bala, nave, fondo, etc.
jugador = None
bala = None
fondo = None
nave = None
menu = None

# Variables de salto
salto = False
salto_altura = 15  # Velocidad inicial de salto
gravedad = 1
en_suelo = True

# Variables de pausa y menú
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
modo_auto = False  # Indica si el modo de juego es automático
modo_manual = False
modo_2_balas = False

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []
datos_modelo_vertical_ball = []
datos_modelo_diagonal_ball = []

# Lista para guardar los datos de velocidad, distancia y salto (target)
datos_modelo = []

# Cargar las imágenes
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]

bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')

# Escalar la imagen de fondo para que coincida con el tamaño de la pantalla
fondo_img = pygame.transform.scale(fondo_img, (w, h))

# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú

# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0

# Variables para la bala
velocidad_bala = -20  # Velocidad de la bala hacia la izquierda
bala_disparada = False

# Variables para la segunda bala
bala2 = pygame.Rect(random.randint(0, w - 16), 0, 16, 16)
velocidad_bala2 = 5  # Velocidad de la bala hacia abajo
bala2_disparada = False

# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w




# Función para disparar la bala
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-10, -4)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True

# Función para reiniciar la posición de la bala
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False

# Función para disparar la segunda bala
def disparar_bala2():
    global bala2_disparada, bala2, velocidad_bala2
    if not bala2_disparada:
        bala2.x = random.randint(0, w - 16)
        bala2.y = 0
        velocidad_bala2 = random.randint(3, 7)  # Velocidad aleatoria hacia abajo
        bala2_disparada = True

# Función para reiniciar la posición de la segunda bala
def reset_bala2():
    global bala2, bala2_disparada
    bala2.x = random.randint(0, w - 16)
    bala2.y = 0
    bala2_disparada = False

# Función para manejar el salto
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True

# Función para actualizar el juego
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2
    global modo_decision_tree, salto

    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1

    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w

    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w

    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))

    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0

    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        reiniciar_juego()  # Terminar el juego y mostrar el menú

    # Mover y dibujar la segunda bala si está en modo 2 o 3 balas
    if modo_2_balas:
        if bala2_disparada:
            bala2.y += velocidad_bala2
        else:
            disparar_bala2()

        # Si la bala2 sale de la pantalla, reiniciar su posición
        if bala2.y > h:
            reset_bala2()

        pantalla.blit(bala_img, (bala2.x, bala2.y))

        # Colisión entre la bala2 y el jugador
        if jugador.colliderect(bala2):
            print("Colisión con bala 2 detectada!")
            reiniciar_juego()

# Función para guardar datos del modelo en modo manual
def guardar_datos():
    global jugador, bala, velocidad_bala, salto, bala2, velocidad_bala2
    global modo_manual, modo_2_balas

    if modo_manual:
        distancia = abs(jugador.x - bala.x)
        salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
        # Guardar velocidad de la bala, distancia al jugador y si saltó o no
        datos_modelo.append((velocidad_bala, distancia, salto_hecho))

    if modo_2_balas:
        distancia = abs(jugador.x - bala.x)
        salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
        # Guardar velocidad de la bala, distancia al jugador y si saltó o no
        datos_modelo.append((velocidad_bala, distancia, salto_hecho))

        distanciaY = abs(jugador.y - bala2.y)
        datos_modelo_vertical_ball.append((velocidad_bala2, distanciaY))


# Función para pausar el juego y guardar los datos
def pausa_juego():
    global pausa, menu_activo
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
        menu_activo = True
        mostrar_menu()
    else:
        print("Juego reanudado.")

# Función para mostrar el menú de opciones
def print_menu_options():
    lineas = [
        "============ MENU =============",
        "",
        "Press D - Auto Mode Decision Tree",
        "Press N - Auto Mode Neural Network",
        "Press R - Auto Mode Linear Regression",
        "Press K - Auto Mode KNN",
        "Press M - Manual Mode",
        "Press S - Save DataSet",
        "Press 2 - Double bullets Mode",
        "Press Q - Exit",
    ]

    # Posición inicial
    x = w // 4
    y = h // 2 - (len(lineas) * 20)  # Ajusta el desplazamiento vertical según el número de líneas

    for linea in lineas:
        texto = fuente.render(linea, True, BLANCO)
        pantalla.blit(texto, (x, y))
        y += 40
    pygame.display.flip()

# Función para mostrar el menú y seleccionar el modo de juego
def mostrar_menu():
    global pausa, menu_activo, modo_auto, modo_manual, modo_2_balas
    global modo_decision_tree, modo_manual, modo_auto, mode_neural_network
    global datos_modelo, datos_modelo_vertical_ball

    pantalla.fill(NEGRO)
    print_menu_options()
    pygame.display.flip()

    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    print("Press m")
                    datos_modelo = []
                    modo_auto = False
                    modo_manual = True
                    modo_auto = False
                    modo_decision_tree = False
                    modo_2_balas = False
                    menu_activo = False
                    # correr = True
                    pausa = False
                elif evento.key == pygame.K_q:
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

    pygame.display.flip()


# Función para reiniciar el juego tras la colisión
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo, bala2_disparada, salto_altura
    global datos_modelo, datos_modelo_vertical_ball, datos_modelo_diagonal_ball

    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    salto_altura = 15  # Restablecer la velocidad de salto
    en_suelo = True
    # Reiniciar la segunda bala
    bala2.x = random.randint(0, w - 16)
    bala2.y = 0
    bala2_disparada = False
    # Mostrar los datos recopilados hasta el momento
    print("Datos recopilados para el modelo: ", datos_modelo)

    # datos_modelo = []

    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo


def run_any_mode(correr):
    global salto, en_suelo, bala_disparada
    global modo_decision_tree, modo_manual, modo_auto
    global bala, velocidad_bala, jugador, prediction_counter
    pygame.display.flip()
    reloj = pygame.time.Clock()
    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    # print('saltando.....')
                    salto = True
                    en_suelo = False
                    salto_altura = 15  # Restablecer la velocidad de salto al iniciar un nuevo salto

                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado.")
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto:
                print('modo manual')
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            # Move right or left
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                jugador.x -= 5
            if keys[pygame.K_RIGHT]:
                jugador.x += 5

            # Mantener al jugador dentro de los límites de la pantalla
            if jugador.x < 0:
                jugador.x = 0
            if jugador.x > w - jugador.width:
                jugador.x = w - jugador.width

            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 60 FPS


def main():
    global salto, en_suelo, bala_disparada
    global modo_decision_tree, modo_manual, modo_auto
    global bala, velocidad_bala, jugador, prediction_counter

    mostrar_menu()  # Mostrar el menú al inicio
    correr = True
    run_any_mode(correr)

    pygame.quit()

if __name__ == "__main__":
    main()
