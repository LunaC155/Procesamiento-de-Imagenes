import cv2
import numpy as np

def detectar_lineas(imagen, umbral=100, min_longitud=100, max_gap=10):
    """
    Detecta líneas rectas en la imagen y las dibuja.
    """
    # 1. Pre-procesamiento: Hough necesita bordes, no colores.
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        # Copia para dibujar resultados a color
        img_salida = imagen.copy()
    else:
        img_gray = imagen
        img_salida = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)

    # 2. Detectar bordes con Canny (paso obligatorio para Hough)
    bordes = cv2.Canny(img_gray, 50, 150, apertureSize=3)

    # 3. Aplicar Hough Probabilístico
    # rho: precisión de distancia (1 pixel)
    # theta: precisión de ángulo (np.pi/180 = 1 grado)
    # threshold: votos mínimos para considerar una línea
    lineas = cv2.HoughLinesP(bordes, 1, np.pi/180, umbral, 
                             minLineLength=min_longitud, 
                             maxLineGap=max_gap)

    # 4. Dibujar líneas detectadas
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            # Dibujar línea verde (0, 255, 0) con grosor 2
            cv2.line(img_salida, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
    return img_salida

def detectar_circulos(imagen, min_dist=20, param1=50, param2=30, min_radio=0, max_radio=0):
    """
    Detecta círculos usando la Transformada de Hough.
    """
    # 1. Convertir a grises y suavizar (vital para evitar falsos círculos)
    if len(imagen.shape) == 3:
        img_gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
        img_salida = imagen.copy()
    else:
        img_gray = imagen
        img_salida = cv2.cvtColor(imagen, cv2.COLOR_GRAY2RGB)

    img_gray = cv2.medianBlur(img_gray, 5)

    # 2. Aplicar Hough Circles
    circulos = cv2.HoughCircles(
        img_gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=min_dist,
        param1=param1,  # Umbral superior de Canny
        param2=param2,  # Umbral para centro del círculo (menor = más círculos falsos)
        minRadius=min_radio, 
        maxRadius=max_radio
    )

    # 3. Dibujar
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            # Dibujar el borde del círculo (Verde)
            cv2.circle(img_salida, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Dibujar el centro (Rojo)
            cv2.circle(img_salida, (i[0], i[1]), 2, (255, 0, 0), 3)

    return img_salida