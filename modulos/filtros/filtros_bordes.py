import cv2
import numpy as np

def aplicar_sobel(imagen):
    """
    Detecta bordes verticales y horizontales y los combina.
    Es resistente al ruido.
    """
    # Asegurar escala de grises para mejor resultado, aunque Sobel funciona en color,
    # es estándar usarlo en intensidad.
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = imagen

    # Gradientes en X e Y (cv2.CV_64F permite valores negativos para detectar bordes oscuros a claros)
    grad_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)

    # Convertir a valor absoluto y uint8
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    # Combinar ambos gradientes
    return cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

def aplicar_laplaciano(imagen):
    """Detecta bordes en todas direcciones usando segunda derivada."""
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        
    dst = cv2.Laplacian(imagen, cv2.CV_64F)
    return cv2.convertScaleAbs(dst)

def aplicar_canny(imagen, umbral_bajo=100, umbral_alto=200):
    """
    El detector de bordes óptimo. 
    Limpia ruido, encuentra intensidad y filtra falsos positivos.
    """
    # Canny necesita una imagen de un solo canal (grises)
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        
    return cv2.Canny(imagen, umbral_bajo, umbral_alto)

def aplicar_prewitt(imagen):
    """
    Similar a Sobel pero con un kernel diferente.
    OpenCV no lo tiene nativo, lo construimos manualmente.
    """
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = imagen

    # Kernels de Prewitt
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])

    img_prewittx = cv2.filter2D(img_gray, -1, kernelx)
    img_prewitty = cv2.filter2D(img_gray, -1, kernely)
    
    return cv2.addWeighted(img_prewittx, 0.5, img_prewitty, 0.5, 0)