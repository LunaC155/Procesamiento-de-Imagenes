import cv2

def _asegurar_grises(imagen):
    """Función auxiliar privada para convertir a grises si es necesario."""
    if len(imagen.shape) == 3:
        return cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    return imagen

def umbral_simple(imagen, valor_umbral=127):
    """
    Si el píxel > umbral -> Blanco, si no -> Negro.
    """
    img_gray = _asegurar_grises(imagen)
    # Retorna tupla (valor_usado, imagen), nos quedamos con la imagen [1]
    _, threshed = cv2.threshold(img_gray, valor_umbral, 255, cv2.THRESH_BINARY)
    return threshed

def umbral_otsu(imagen):
    """
    Calcula automáticamente el mejor umbral basándose en el histograma bimodal.
    Ideal cuando hay un contraste claro entre fondo y objeto.
    """
    img_gray = _asegurar_grises(imagen)
    # THRESH_OTSU se suma a THRESH_BINARY
    _, threshed = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshed

def umbral_adaptativo(imagen):
    """
    Calcula umbrales locales para diferentes regiones.
    Ideal para imágenes con iluminación desigual (sombras).
    """
    img_gray = _asegurar_grises(imagen)
    threshed = cv2.adaptiveThreshold(
        img_gray, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, # Tamaño de bloque (vecindario)
        2   # Constante a restar
    )
    return threshed