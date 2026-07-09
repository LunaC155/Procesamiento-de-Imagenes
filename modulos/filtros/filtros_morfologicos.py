import cv2
import numpy as np

def _get_kernel(tamano):
    return np.ones((tamano, tamano), np.uint8)

def erosion(imagen, tamano=5):
    return cv2.erode(imagen, _get_kernel(tamano), iterations=1)

def dilatacion(imagen, tamano=5):
    return cv2.dilate(imagen, _get_kernel(tamano), iterations=1)

def apertura(imagen, tamano=5):
    """Erosión seguida de dilatación. Elimina ruido blanco pequeño."""
    return cv2.morphologyEx(imagen, cv2.MORPH_OPEN, _get_kernel(tamano))

def cierre(imagen, tamano=5):
    """Dilatación seguida de erosión. Cierra agujeros negros pequeños."""
    return cv2.morphologyEx(imagen, cv2.MORPH_CLOSE, _get_kernel(tamano))

def gradiente_morfologico(imagen, tamano=5):
    """Diferencia entre dilatación y erosión (Bordes)."""
    return cv2.morphologyEx(imagen, cv2.MORPH_GRADIENT, _get_kernel(tamano))

def top_hat(imagen, tamano=9):
    """Revela elementos brillantes en fondo oscuro."""
    return cv2.morphologyEx(imagen, cv2.MORPH_TOPHAT, _get_kernel(tamano))

def black_hat(imagen, tamano=9):
    """Revela elementos oscuros en fondo brillante."""
    return cv2.morphologyEx(imagen, cv2.MORPH_BLACKHAT, _get_kernel(tamano))