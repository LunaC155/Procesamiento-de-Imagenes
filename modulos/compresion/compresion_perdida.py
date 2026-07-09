import cv2
import numpy as np

def simular_jpeg(imagen, calidad=10):
    """
    Comprime y descomprime en memoria para simular pérdida.
    Calidad: 1 (peor) a 100 (mejor).
    """
    # Codificar a formato jpg en memoria
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), calidad]
    result, encimg = cv2.imencode('.jpg', cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR), encode_param)
    
    # Decodificar de vuelta
    decimg = cv2.imdecode(encimg, 1)
    return cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)