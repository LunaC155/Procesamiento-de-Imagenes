import cv2
import numpy as np

def obtener_espectro(imagen):
    """
    Calcula la Transformada de Fourier Discreta y retorna su espectro de magnitud.
    Visualiza las frecuencias: el centro son frecuencias bajas, los bordes altas.
    """
    # 1. Convertir a grises si es necesario
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    else:
        img_gray = imagen

    # 2. Aplicar FFT (Fast Fourier Transform) con Numpy
    f = np.fft.fft2(img_gray)
    
    # 3. Shift: Mover el componente de frecuencia cero (DC) al centro de la imagen
    fshift = np.fft.fftshift(f)
    
    # 4. Calcular Magnitud: 20*log(abs(f)) 
    # Usamos logaritmo porque el rango dinámico es enorme y si no, solo veríamos un punto blanco
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1e-5) # +1e-5 evita log(0)
    
    # 5. Normalizar a 0-255 para poder mostrarlo como imagen
    magnitude_spectrum = cv2.normalize(magnitude_spectrum, None, 0, 255, cv2.NORM_MINMAX)
    
    return np.uint8(magnitude_spectrum)