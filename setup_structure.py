import os

structure = [
    "datos/imagenes_entrada",
    "datos/resultados",
    "modulos/filtros",
    "modulos/transformadas",
    "modulos/color",
    "modulos/geometricas",
    "modulos/segmentacion",
    "modulos/compresion",
    "modulos/utilidades",
    "modulos/interfaces",
    "configuracion"
]

files = {
    "": ["main.py", "interfaz_grafica.py", "requirements.txt"],
    "modulos": ["__init__.py"],
    "modulos/filtros": ["__init__.py", "filtros_suavizado.py", "filtros_realce.py", "filtros_bordes.py", "filtros_morfologicos.py"],
    "modulos/transformadas": ["__init__.py", "transformada_fourier.py", "transformada_hough.py"],
    "modulos/color": ["__init__.py", "conversion_color.py", "ajuste_color.py"],
    "modulos/geometricas": ["__init__.py", "transformaciones_basicas.py"],
    "modulos/segmentacion": ["__init__.py", "umbralizacion.py", "algoritmo_canny.py"],
    "modulos/utilidades": ["__init__.py", "carga_guardado.py", "visualizacion.py"],
    "configuracion": ["__init__.py", "configuracion.py", "estilos.py"]
}

def create_project():
    # Crear carpetas
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        print(f"Carpeta creada: {folder}")

    # Crear archivos
    for folder, file_list in files.items():
        for filename in file_list:
            path = os.path.join(folder, filename)
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    pass
                print(f"Archivo creado: {path}")

if __name__ == "__main__":
    create_project()
    print("\n✅ Estructura del proyecto generada con éxito.")