import cv2
import numpy as np
from tensorflow.keras.models import load_model
import os
import skfuzzy as fuzz

# Cargar etiquetas dinámicamente desde las carpetas de imagenes_procesadas/train
ruta_dataset = "imagenes_procesadas"
ruta_emociones = os.path.join(ruta_dataset, "train")
emotion_labels = sorted([d for d in os.listdir(ruta_emociones) if os.path.isdir(os.path.join(ruta_emociones, d))])

# Cargar modelo
model_path = "Modelos/reconocedor_emociones.h5"
model = load_model(model_path)
image_size = (48, 48)

# Cargar clasificador Haar
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Diccionario de traducción de etiquetas (ejemplo)
traducciones = {
    "anger": "enojado",
    "happy": "feliz",
    "sad": "triste",
}

def predecir_emocion(roi):
    roi = cv2.resize(roi, image_size)
    roi = roi.reshape(1, 48, 48, 1) / 255.0
    prediction = model.predict(roi)[0]
    idx = np.argmax(prediction)
    etiqueta = emotion_labels[idx]
    etiqueta_mostrar = traducciones.get(etiqueta, etiqueta)
    return etiqueta_mostrar, np.max(prediction)

def reconocimiento_tiempo_real():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            emotion, confidence = predecir_emocion(roi_gray)
            text = f"{emotion} ({confidence*100:.1f}%)"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.putText(frame, 'Presione "q" para salir', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 1)
        cv2.imshow('Reconocimiento de Emociones', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    reconocimiento_tiempo_real()
