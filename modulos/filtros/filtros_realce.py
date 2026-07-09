import cv2
import numpy as np

def aplicar_sharpen(imagen):
    """Aumenta la nitidez usando un kernel clásico."""
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(imagen, -1, kernel)

def aplicar_paso_alto(imagen):
    """Filtro de paso alto (resta la imagen suavizada de la original)."""
    # Usamos un kernel que elimina la media (DC) y deja bordes
    kernel = np.array([[-1, -1, -1],
                       [-1,  8, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(imagen, -1, kernel)

def unsharp_mask(imagen, sigma=1.0, strength=1.5):
    """
    Máscara de enfoque: Realza bordes restando una versión desenfocada.
    Formula: Original + (Original - Suavizada) * fuerza
    """
    gaussian = cv2.GaussianBlur(imagen, (0, 0), sigma)
    return cv2.addWeighted(imagen, 1.0 + strength, gaussian, -strength, 0)