import cv2
import numpy as np
from scipy.linalg import hadamard

def aplicar_walsh_hadamard(imagen):
    """
    Aplica WHT. Nota: La imagen debe ser redimensionada a potencia de 2.
    Se usa una aproximación o redimensión para visualización.
    """
    if len(imagen.shape) == 3:
        img = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img = imagen
        
    # Redimensionar a la potencia de 2 más cercana (ej 256x256) para que funcione Hadamard
    h, w = img.shape
    potencia = int(2**np.floor(np.log2(min(h, w))))
    img_resized = cv2.resize(img, (potencia, potencia))
    
    # Crear matriz Hadamard
    H = hadamard(potencia)
    
    # Aplicar transformación: H * img * H
    img_float = np.float64(img_resized)
    wht = np.dot(np.dot(H, img_float), H)
    
    # Visualización
    res = np.log(np.abs(wht) + 1)
    res = cv2.normalize(res, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(res)