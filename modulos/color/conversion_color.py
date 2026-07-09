import cv2

def a_escala_grises(imagen_rgb):
    """
    Convierte una imagen RGB a Escala de Grises.
    Retorna una imagen de 1 canal.
    """
    if len(imagen_rgb.shape) == 3:
        return cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2GRAY)
    return imagen_rgb

def a_rgb(imagen_bgr):
    """Convierte BGR (formato nativo OpenCV) a RGB."""
    return cv2.cvtColor(imagen_bgr, cv2.COLOR_BGR2RGB)

def a_hsv(imagen_rgb):
    """Convierte RGB a espacio de color HSV."""
    return cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2HSV)