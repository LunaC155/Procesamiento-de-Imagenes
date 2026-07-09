from PIL import Image, ImageTk
import numpy as np

def convertir_a_tk(imagen_np, ancho_max=800, alto_max=600):
    """
    Convierte una imagen numpy (RGB o Grises) a formato compatible con Tkinter.
    Maneja redimensionamiento para vista previa.
    """
    if imagen_np is None:
        return None

    # Convertir Numpy a Pillow Image
    # Si es escala de grises (2 dimensiones), Pillow lo detecta, 
    # pero debemos asegurar el modo correcto.
    if len(imagen_np.shape) == 2:
        img_pil = Image.fromarray(imagen_np, mode='L') # L = Luminance (Grises)
    else:
        img_pil = Image.fromarray(imagen_np, mode='RGB')

    # Redimensionar manteniendo aspecto (thumbnail)
    img_pil.thumbnail((ancho_max, alto_max), Image.Resampling.LANCZOS)
    
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk