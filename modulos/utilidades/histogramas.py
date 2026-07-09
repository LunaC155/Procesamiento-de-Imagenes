import cv2
from matplotlib import pyplot as plt

def mostrar_histograma(imagen):
    """
    Calcula y muestra el histograma de la imagen usando Matplotlib.
    Detecta si es color o escala de grises.
    """
    plt.figure(num='Histograma de Imagen')
    plt.title("Histograma de Intensidad")
    plt.xlabel("Intensidad (0-255)")
    plt.ylabel("Cantidad de Píxeles")

    if len(imagen.shape) == 2:
        # Caso Escala de Grises
        hist = cv2.calcHist([imagen], [0], None, [256], [0, 256])
        plt.plot(hist, color='black')
        plt.xlim([0, 256])
        
    elif len(imagen.shape) == 3:
        # Caso Color (Separa canales R, G, B)
        colors = ('r', 'g', 'b')
        # OpenCV lee en BGR, pero en la app trabajamos en RGB.
        # Asumimos que recibimos RGB.
        for i, color in enumerate(colors):
            hist = cv2.calcHist([imagen], [i], None, [256], [0, 256])
            plt.plot(hist, color=color)
            plt.xlim([0, 256])

    plt.grid()
    plt.show()