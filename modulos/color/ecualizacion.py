import cv2

def ecualizar_histograma(imagen):
    """
    Aplica ecualización de histograma.
    Si es color, convierte a YUV, ecualiza Y (Luminancia) y reconvierte.
    """
    if len(imagen.shape) == 3:
        img_yuv = cv2.cvtColor(imagen, cv2.COLOR_RGB2YUV)
        # Ecualizar solo el canal Y
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
    else:
        return cv2.equalizeHist(imagen)