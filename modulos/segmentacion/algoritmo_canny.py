import cv2
import numpy as np

def aplicar_canny(imagen, umbral_bajo=50, umbral_alto=150):
    """
    Implementación del algoritmo Canny para detección de bordes.
    Incluye pre-procesamiento de reducción de ruido.
    
    Args:
        imagen: Imagen de entrada (RGB o Grises)
        umbral_bajo: Límite inferior para histéresis
        umbral_alto: Límite superior para histéresis
    """
    # 1. Convertir a escala de grises si es necesario
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = imagen

    # 2. Aplicar Suavizado Gaussiano (Paso crucial de Canny para reducir ruido)
    # Un kernel de 5x5 es estándar para este proceso
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1.4)

    # 3. Aplicar Canny
    # Canny usa internamente Sobel y supresión de no-máximos
    bordes = cv2.Canny(img_blur, umbral_bajo, umbral_alto)

    return bordes