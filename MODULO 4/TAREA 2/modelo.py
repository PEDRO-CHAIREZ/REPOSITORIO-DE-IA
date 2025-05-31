from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

def crear_modelo(input_shape=(48, 48, 1), num_classes=5):
    model = Sequential([
        # Primera capa convolucional
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(pool_size=(2, 2)),
        # Segunda capa convolucional
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

ruta_dataset = 'imagenes_procesadas'  # Especifica la ruta a tu dataset aquí
emotion_labels = sorted([d for d in os.listdir(ruta_dataset) if os.path.isdir(os.path.join(ruta_dataset, d))])
