import cv2

def guardar_png_temp(imagen):
    """
    Guarda temporalmente en PNG (sin pérdida) y recarga.
    """
    # En un flujo real, esto sería guardar a disco.
    # Aquí simulamos el ciclo. PNG usa compresión ZIP sin pérdida.
    result, encimg = cv2.imencode('.png', cv2.cvtColor(imagen, cv2.COLOR_RGB2BGR))
    decimg = cv2.imdecode(encimg, 1)
    return cv2.cvtColor(decimg, cv2.COLOR_BGR2RGB)