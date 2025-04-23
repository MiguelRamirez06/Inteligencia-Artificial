import cv2
import mediapipe as mp
import numpy as np

# Inicializar FaceMesh y Drawing
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1, color=(0, 255, 0))

# Función para calcular distancia euclidiana
def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

# Función para determinar emoción
def detectar_emocion(landmarks, w, h):
    puntos = lambda idx: (int(landmarks[idx].x * w), int(landmarks[idx].y * h))

    boca_superior = puntos(13)
    boca_inferior = puntos(14)
    labio_izq = puntos(61)
    labio_der = puntos(291)
    ojo_izq_sup = puntos(159)
    ojo_izq_inf = puntos(145)
    ojo_der_sup = puntos(386)
    ojo_der_inf = puntos(374)
    ceja_izq = puntos(65)
    ceja_der = puntos(295)
    entrecejo = puntos(168)

    apertura_boca = distance(boca_superior, boca_inferior)
    sonrisa = distance(labio_izq, labio_der)
    apertura_ojo_izq = distance(ojo_izq_sup, ojo_izq_inf)
    apertura_ojo_der = distance(ojo_der_sup, ojo_der_inf)
    altura_cejas = (distance(ceja_izq, entrecejo) + distance(ceja_der, entrecejo)) / 2

    emocion = "Neutral"
    if apertura_boca > 20 and apertura_ojo_izq < 10 and apertura_ojo_der < 10:
        emocion = "Alegria"
    elif altura_cejas > 30 and apertura_boca < 15:
        emocion = "Tristeza"
    elif apertura_boca > 25 and apertura_ojo_izq > 15 and apertura_ojo_der > 15:
        emocion = "Sorpresa"
    elif altura_cejas < 20 and apertura_boca > 15:
        emocion = "Enojo"

    return emocion

# Captura de video
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            emocion = detectar_emocion(face_landmarks.landmark, w, h)

            # Dibujar landmarks en el rostro
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec
            )

            # Mostrar la emoción detectada
            cv2.putText(frame, f'Emocion: {emocion}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1.2, (0, 255, 0), 2)

    cv2.imshow("Detector de Emociones", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
