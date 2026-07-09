import cv2
import numpy as np

def rotar_imagen(imagen, grados):
    """
    Rota la imagen alrededor de su centro.
    Args:
        grados: Angulo de rotación (positivo = anti-horario).
    """
    (h, w) = imagen.shape[:2]
    centro = (w // 2, h // 2)

    # Crear matriz de rotación
    M = cv2.getRotationMatrix2D(centro, grados, 1.0)
    
    # Aplicar transformación
    # warpAffine mueve los píxeles según la matriz M
    return cv2.warpAffine(imagen, M, (w, h))

def escalar_imagen(imagen, porcentaje):
    """
    Redimensiona la imagen.
    Args:
        porcentaje: Entero (ej. 50 para 50%, 200 para 200%).
    """
    scale_percent = porcentaje / 100
    width = int(imagen.shape[1] * scale_percent)
    height = int(imagen.shape[0] * scale_percent)
    dim = (width, height)
    
    # INTER_AREA es mejor para reducir, INTER_LINEAR para agrandar
    interpolacion = cv2.INTER_AREA if porcentaje < 100 else cv2.INTER_LINEAR
    
    return cv2.resize(imagen, dim, interpolation=interpolacion)

def voltear_imagen(imagen, codigo):
    """
    Espejo de la imagen.
    Args:
        codigo: 0 (vertical), 1 (horizontal), -1 (ambos).
    """
    return cv2.flip(imagen, codigo)

def traslacion(imagen, x, y):
    """Mueve la imagen x píxeles a la derecha y y píxeles abajo."""
    (h, w) = imagen.shape[:2]
    # Matriz de traslación [[1, 0, x], [0, 1, y]]
    M = np.float32([[1, 0, x], [0, 1, y]])
    return cv2.warpAffine(imagen, M, (w, h))