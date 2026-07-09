import cv2
import sys

def calcular_tasa_compresion(imagen_original, calidad_jpg):
    """Retorna el tamaño estimado en KB y la tasa de compresión."""
    # Tamaño sin comprimir (aprox en RAM)
    tamano_raw = imagen_original.nbytes
    
    # Tamaño comprimido
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), calidad_jpg]
    result, encimg = cv2.imencode('.jpg', imagen_original, encode_param)
    tamano_comp = encimg.nbytes
    
    ratio = tamano_raw / tamano_comp
    return tamano_comp / 1024, ratio # KB, Ratios