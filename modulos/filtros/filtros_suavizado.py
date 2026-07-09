import cv2

def aplicar_promedio(imagen, kernel_size=5):
    """Suavizado por promedio (blur simple)."""
    return cv2.blur(imagen, (kernel_size, kernel_size))

def aplicar_gaussiano(imagen, kernel_size=5):
    """
    Suavizado Gaussiano.
    kernel_size debe ser impar (3, 5, 7...).
    """
    if kernel_size % 2 == 0: kernel_size += 1 # Asegurar impar
    return cv2.GaussianBlur(imagen, (kernel_size, kernel_size), 0)

def aplicar_mediana(imagen, kernel_size=5):
    """
    Filtro de mediana (muy bueno para ruido tipo 'sal y pimienta').
    kernel_size debe ser impar.
    """
    if kernel_size % 2 == 0: kernel_size += 1
    return cv2.medianBlur(imagen, kernel_size)

def aplicar_bilateral(imagen, d=9, sigma_color=75, sigma_space=75):
    """
    Filtro Bilateral: Suaviza texturas pero mantiene bordes afilados.
    Es más lento pero da mejores resultados visuales.
    """
    return cv2.bilateralFilter(imagen, d, sigma_color, sigma_space)