import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

def cargar_imagen_dialogo():
    """Abre un cuadro de diálogo para seleccionar imagen."""
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
    )
    if ruta:
        # Leer con OpenCV (BGR)
        img_bgr = cv2.imread(ruta)
        # Convertir a RGB para visualización correcta
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        return img_rgb, ruta
    return None, None

def convertir_a_tk(imagen_rgb, ancho_max=800, alto_max=600):
    """Convierte array numpy a imagen compatible con Tkinter y redimensiona para vista previa."""
    img_pil = Image.fromarray(imagen_rgb)
    
    # Redimensionar manteniendo aspecto (thumbnail)
    img_pil.thumbnail((ancho_max, alto_max))
    
    img_tk = ImageTk.PhotoImage(img_pil)
    return img_tk

def guardar_imagen_dialogo(imagen_rgb):
    """
    Abre cuadro de diálogo para guardar la imagen actual.
    Convierte RGB a BGR antes de guardar con OpenCV.
    """
    if imagen_rgb is None:
        return
        
    ruta = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")],
        title="Guardar imagen como"
    )
    
    if ruta:
        # OpenCV guarda en BGR, así que convertimos de vuelta
        # Si la imagen es grises (2 dimensiones), no necesita conversión
        if len(imagen_rgb.shape) == 3:
            img_guardar = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2BGR)
        else:
            img_guardar = imagen_rgb
            
        cv2.imwrite(ruta, img_guardar)
        return True
    return False