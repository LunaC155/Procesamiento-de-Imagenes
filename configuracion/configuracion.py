import os

# Rutas absolutas para evitar errores
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_IMAGENES = os.path.join(BASE_DIR, "datos", "imagenes_entrada")
RUTA_RESULTADOS = os.path.join(BASE_DIR, "datos", "resultados")

# Configuración de Ventana
APP_NOMBRE = "Procesador de Imágenes Pro"
TAMAÑO_VENTANA = "1200x800"