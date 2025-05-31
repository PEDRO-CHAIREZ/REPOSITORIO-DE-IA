import os
from PIL import Image, ImageEnhance

input_root = 'emociones'
output_root = 'imagenes_procesadas'
image_size = (48, 48)  # Tamaño estándar para el modelo

def preprocess_image(img):
    img = img.resize(image_size)
    variations = []
    variations.append(('original', img))
    enhancer = ImageEnhance.Brightness(img)
    variations.append(('brillo_alto', enhancer.enhance(1.5)))
    variations.append(('brillo_bajo', enhancer.enhance(0.5)))
    variations.append(('rot_90', img.rotate(90)))
    variations.append(('brillo_muy_bajo', enhancer.enhance(0.2)))
    return variations

for split in os.listdir(input_root):  # split = train, test, validacion
    split_path = os.path.join(input_root, split)
    if not os.path.isdir(split_path):
        continue
    for emotion in os.listdir(split_path):  # emotion = sad, angre, happy
        emotion_path = os.path.join(split_path, emotion)
        if not os.path.isdir(emotion_path):
            continue
        print(f"Procesando carpeta: {split}/{emotion}")
        for filename in os.listdir(emotion_path):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
            img_path = os.path.join(emotion_path, filename)
            try:
                img = Image.open(img_path).convert('RGB')
                processed_versions = preprocess_image(img)
                for variation, processed_img in processed_versions:
                    new_filename = f"{os.path.splitext(filename)[0]}_{variation}.jpg"
                    save_folder = os.path.join(output_root, split, emotion)
                    os.makedirs(save_folder, exist_ok=True)
                    save_path = os.path.join(save_folder, new_filename)
                    processed_img.save(save_path)
            except Exception as e:
                print(f"Error procesando {img_path}: {e}")

print(f"Proceso completado. Imágenes procesadas y guardadas en {output_root}.")
