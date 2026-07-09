import cv2
import numpy as np

def segmentar_kmeans(imagen, k=3):
    """
    Agrupa los colores de la imagen en 'k' colores dominantes.
    """
    # 1. Convertir datos a float32 y a una columna (flatten)
    pixel_vals = imagen.reshape((-1, 3))
    pixel_vals = np.float32(pixel_vals)
    
    # 2. Criterios de parada (epsilon o iteraciones)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    
    # 3. Aplicar K-means
    ret, label, center = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # 4. Reconstruir imagen
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((imagen.shape))