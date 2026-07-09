import cv2
import numpy as np

def calcular_histograma_color(imagen):
    """Retorna los datos de histograma para R, G, B."""
    colors = ('r', 'g', 'b')
    datos = {}
    for i, color in enumerate(colors):
        # CalcHist retorna un array (256, 1)
        hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
        datos[color] = hist
    return datos