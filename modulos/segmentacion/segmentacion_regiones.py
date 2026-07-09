import cv2
import numpy as np

def aplicar_watershed(imagen):
    """
    Algoritmo Watershed automático basado en distancia.
    """
    img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Remover ruido
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Área de fondo segura
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Área de objeto segura (Distancia transform)
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

    # Región desconocida (Bordes)
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Etiquetado
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1 # Asegurar fondo es 1, no 0
    markers[unknown == 255] = 0 # Desconocido es 0

    # Aplicar Watershed
    # Watershed necesita imagen de 3 canales BGR/RGB
    img_copy = imagen.copy()
    cv2.watershed(img_copy, markers)
    
    # Dibujar bordes en rojo (-1 indica barreras)
    img_copy[markers == -1] = [255, 0, 0]
    
    return img_copy