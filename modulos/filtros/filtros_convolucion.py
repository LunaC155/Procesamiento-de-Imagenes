import cv2
import numpy as np

def aplicar_emboss(imagen):
    """Efecto de relieve."""
    kernel = np.array([[-2, -1, 0],
                       [-1,  1, 1],
                       [ 0,  1, 2]])
    # Sumamos 128 para que el gris medio sea el fondo neutro
    res = cv2.filter2D(imagen, -1, kernel) + 128
    # Normalizamos para que no pase de 255
    return np.clip(res, 0, 255).astype(np.uint8)

def kernel_personalizado(imagen, kernel_matrix):
    """Aplica una matriz de convolución definida por el usuario."""
    return cv2.filter2D(imagen, -1, kernel_matrix)