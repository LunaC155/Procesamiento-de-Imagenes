import cv2
import numpy as np

def aplicar_sesgado(imagen, factor=0.2):
    """
    Aplica 'Shear' (deformación lateral).
    """
    h, w = imagen.shape[:2]
    # Matriz de afinidad para Shear en X
    M = np.float32([[1, factor, 0], 
                    [0, 1,      0]])
    
    # Calcular nuevo ancho para que no se corte
    nuevo_w = w + int(h * factor)
    
    return cv2.warpAffine(imagen, M, (nuevo_w, h))

def correccion_perspectiva_demo(imagen):
    """
    Aplica una transformación de perspectiva fija como demostración.
    (Normalmente requiere 4 puntos de entrada del mouse).
    """
    h, w = imagen.shape[:2]
    
    puntos_origen = np.float32([[0,0], [w,0], [0,h], [w,h]])
    
    # Simulamos que la parte superior se encoge (efecto Star Wars)
    offset = w * 0.2
    puntos_destino = np.float32([[offset, 0], [w-offset, 0], [0, h], [w, h]])
    
    M = cv2.getPerspectiveTransform(puntos_origen, puntos_destino)
    return cv2.warpPerspective(imagen, M, (w, h))