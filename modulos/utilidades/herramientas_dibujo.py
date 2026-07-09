import cv2
import numpy as np

def dibujar_rectangulo(imagen, x, y, w, h, color=(255, 0, 0), grosor=2): # <--- Asegura que tenga grosor
    img_copia = imagen.copy()
    cv2.rectangle(img_copia, (x, y), (x+w, y+h), color, grosor)
    return img_copia

def dibujar_circulo(imagen, centro_x, centro_y, radio, color=(0, 255, 0), grosor=2):
    img_copia = imagen.copy()
    cv2.circle(img_copia, (centro_x, centro_y), radio, color, grosor)
    return img_copia

def escribir_texto(imagen, texto, x, y, color=(255, 255, 255)):
    img_copia = imagen.copy()
    cv2.putText(img_copia, texto, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                1, color, 2, cv2.LINE_AA)
    return img_copia
def relleno_floodfill(imagen, x, y, color_nuevo, tolerancia=10):
    """
    Rellena una región de color similar (Bote de pintura).
    """
    im_in = imagen.copy()
    h, w = im_in.shape[:2]
    
    # Máscara necesaria para floodFill (debe ser 2 píxeles más grande que la imagen)
    mask = np.zeros((h+2, w+2), np.uint8)
    
    # Definir rango de tolerancia (lo loDIFF y upDiff)
    lo = (tolerancia,)*3
    up = (tolerancia,)*3
    
    # Floodfill funciona en BGR/RGB directamente
    # Flags: 4 u 8 conectividad | (255 << 8) para llenar la máscara | FLOODFILL_FIXED_RANGE
    flags = 4 | (255 << 8) | cv2.FLOODFILL_FIXED_RANGE
    
    cv2.floodFill(im_in, mask, (x, y), color_nuevo, lo, up, flags)
    
    return im_in