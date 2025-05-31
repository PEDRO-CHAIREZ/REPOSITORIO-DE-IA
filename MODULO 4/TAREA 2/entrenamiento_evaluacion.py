import os
import numpy as np
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from modelo import crear_modelo

def cargar_datos(ruta, image_size=(48, 48)):
    X, y = [], []
    etiquetas = sorted(os.listdir(ruta))
    etiqueta_dict = {nombre: idx for idx, nombre in enumerate(etiquetas)}
    for etiqueta in etiquetas:
        carpeta = os.path.join(ruta, etiqueta)
        if not os.path.isdir(carpeta):
            continue
        for archivo in os.listdir(carpeta):
            if archivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                img_path = os.path.join(carpeta, archivo)
                img = load_img(img_path, color_mode='grayscale', target_size=image_size)
                X.append(img_to_array(img))
                y.append(etiqueta_dict[etiqueta])
    X = np.array(X).astype('float32') / 255.0
    y = np.array(y)
    return X, y, etiquetas

# Cargar datos
base_dir = "imagenes_procesadas"
train_X, train_y, etiquetas = cargar_datos(os.path.join(base_dir, "train"))
val_X, val_y, _ = cargar_datos(os.path.join(base_dir, "validation"))
test_X, test_y, _ = cargar_datos(os.path.join(base_dir, "test"))

# One-hot encoding para entrenamiento y validación
train_y_cat = to_categorical(train_y, num_classes=len(etiquetas))
val_y_cat = to_categorical(val_y, num_classes=len(etiquetas))

# Crear y entrenar modelo
modelo = crear_modelo(num_classes=len(etiquetas))
modelo.fit(train_X, train_y_cat, validation_data=(val_X, val_y_cat), epochs=15)

# Evaluar en test y matriz de confusión
y_pred = modelo.predict(test_X)
y_pred_labels = np.argmax(y_pred, axis=1)

cm = confusion_matrix(test_y, y_pred_labels)
print("Matriz de confusión:")
print(cm)
print("\nReporte de clasificación:")
print(classification_report(test_y, y_pred_labels, target_names=etiquetas))

# Visualización de la matriz de confusión
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=etiquetas, yticklabels=etiquetas)
plt.xlabel('Predicción')
plt.ylabel('Real')
plt.title('Matriz de Confusión')
plt.show()