import cv2
import numpy as np

def aplicar_dct(imagen):
    """
    Aplica DCT y retorna la visualización logarítmica.
    DCT funciona mejor en Grises y float.
    """
    # 1. Convertir a grises y float32
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = imagen
        
    img_float = np.float32(img_gray) / 255.0
    
    # 2. Aplicar DCT
    dct = cv2.dct(img_float)
    
    # 3. Visualización (Log para ver detalles)
    res = np.log(np.abs(dct) + 1e-5)
    res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(res)

def inversa_dct(dct_data):
    """Ejemplo de reconstrucción (requiere datos float originales)."""
    idct = cv2.idct(dct_data)
    res = cv2.normalize(idct, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(res)