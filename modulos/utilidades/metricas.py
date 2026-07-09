import cv2
import numpy as np

def calcular_mse(img1, img2):
    """Error Cuadrático Medio."""
    # Asegurar mismo tamaño
    if img1.shape != img2.shape: return -1
    
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1])
    return err

def calcular_psnr(img1, img2):
    """Peak Signal-to-Noise Ratio (dB). Mayor es mejor."""
    mse = calcular_mse(img1, img2)
    if mse == 0: return float('inf')
    if mse == -1: return 0
    
    pixel_max = 255.0
    return 20 * np.log10(pixel_max / np.sqrt(mse))