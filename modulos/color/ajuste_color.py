import cv2
import numpy as np

def ajustar_brillo_contraste(imagen, brillo=0, contraste=0):
    """
    Brillo: -100 a 100
    Contraste: -100 a 100
    """
    # Mapear contraste de [-100, 100] a [0.0, 2.0]
    alpha = (contraste + 100) / 100.0 
    beta = brillo
    return cv2.convertScaleAbs(imagen, alpha=alpha, beta=beta)

def ajustar_saturacion(imagen, incremento=1.0):
    """
    Incremento: 0.0 (grises) a 2.0+ (muy saturado). 1.0 es original.
    """
    hsv = cv2.cvtColor(imagen, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    
    # Usar float para evitar desbordamiento, luego clip
    s = s.astype(np.float32) * incremento
    s = np.clip(s, 0, 255).astype(np.uint8)
    
    hsv_final = cv2.merge([h, s, v])
    return cv2.cvtColor(hsv_final, cv2.COLOR_HSV2RGB)