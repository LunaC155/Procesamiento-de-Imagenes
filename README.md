# 📸 Procesador de Imágenes

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

Una aplicación de escritorio avanzada para el procesamiento digital de imágenes, desarrollada íntegramente en Python. Este proyecto combina potentes algoritmos matemáticos y de visión por computadora con una interfaz gráfica moderna e interactiva, diseñada para fines tanto educativos como profesionales.

---

## 🚀 Características Principales

Esta aplicación cubre un amplio espectro de técnicas de visión artificial y procesamiento de imágenes, organizadas de la siguiente manera:

### 1. 🎨 Interfaz y Herramientas Interactivas
* **Diseño Moderno:** Interfaz de usuario basada en `ttkbootstrap` con tema oscuro ("Superhero") para una mejor ergonomía visual.
* **Dibujo en Tiempo Real:** Previsualización dinámica de formas geométricas (Rectángulos, Círculos) mediante *Double Buffering*.
* **Cursores Dinámicos:** Adaptación visual del cursor según la herramienta seleccionada (Lápiz, Relleno, Cruz, etc.).
* **Historial Completo:** Sistema robusto de **Deshacer (Ctrl+Z)** y **Rehacer (Ctrl+Y)** sin límite prestablecido.
* **Navegación Avanzada:** Funcionalidades de zoom y paneo optimizadas para la inspección detallada de imágenes grandes.

### 2. 🛠️ Filtros Espaciales y Morfológicos
* **Suavizado y Reducción de Ruido:** Filtros Promedio, Gaussiano, de Mediana y Bilateral (suavizado que respeta los bordes).
* **Realce:** Enfoque (Sharpen), Filtro de Paso Alto y Máscara de Desenfoque (Unsharp Mask).
* **Detección de Bordes:** Canny, Sobel, Prewitt y Laplaciano.
* **Morfología Matemática:** Operaciones de Erosión, Dilatación, Apertura, Cierre, Top Hat, Black Hat y Gradiente Morfológico.

### 3. 📊 Transformadas y Frecuencias
* **Transformada de Fourier (FFT):** Análisis y visualización del espectro de magnitud de frecuencias.
* **Transformada de Hough:** Detección automatizada de líneas rectas y circunferencias.
* **Otras Transformadas:** Discreta del Coseno (DCT) y Walsh-Hadamard para el análisis de señales.

### 4. 🌈 Procesamiento de Color
* **Espacios de Color:** Conversión precisa a escala de grises (luminancia).
* **Ajustes Manuales:** Control paramétrico de Brillo, Contraste y Saturación.
* **Mejora Automática:** Ecualización de histograma para la corrección del contraste global.

### 5. ✂️ Segmentación y Geometría
* **Umbralización:** Métodos adaptativos y algoritmo de Otsu para cálculo automático del umbral óptimo.
* **Segmentación Avanzada:** Algoritmo *Watershed* y agrupamiento de color mediante *K-Means Clustering*.
* **Transformaciones Geométricas:** Operaciones de rotación, escalado, traslación, volteo (H/V), sesgado (Shear) y corrección de perspectiva.

### 6. 📉 Análisis y Compresión
* **Simulación JPEG:** Entorno de pruebas para la visualización de artefactos de compresión con pérdida.
* **Métricas de Calidad:** Cálculo instantáneo de **MSE** (Error Cuadrático Medio) y **PSNR** (Relación Señal-Ruido) respecto a la imagen original.
* **Análisis Estadístico:** Generación y visualización de histogramas de intensidad (RGB y Grises).

---

## 💻 Requisitos del Sistema e Instalación

* **Sistema Operativo:** Compatible con Windows, macOS y Linux.
* **Intérprete:** Python 3.8 o superior.

### Instalación Rápida

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/TuUsuario/procesador-imagenes.git
   cd procesador-imagenes
   ```

2. **Crear y activar un entorno virtual (Recomendado)**
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate

   # En macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

---

## 📂 Arquitectura del Proyecto

El proyecto sigue principios de diseño modular para facilitar su mantenimiento y escalabilidad:

```text
procesador-imagenes/
├── main.py                     # Punto de entrada de la aplicación
├── interfaz_grafica.py         # Lógica de la GUI, eventos y menús
├── requirements.txt            # Dependencias del proyecto
├── configuracion/              # Ajustes globales y estilos visuales
├── modulos/                    # Núcleo de procesamiento de imágenes
│   ├── filtros/                # Operaciones espaciales y morfológicas
│   ├── transformadas/          # Procesamiento en el dominio de la frecuencia
│   ├── color/                  # Ajustes y conversiones de espacios de color
│   ├── geometricas/            # Transformaciones espaciales
│   ├── segmentacion/           # Detección y agrupación de píxeles
│   ├── compresion/             # Algoritmos de pérdida y métricas
│   └── utilidades/             # Herramientas de E/S, dibujo y visualización
└── datos/                      # Almacenamiento local (imágenes de prueba)
```

---

## 👨‍💻 Autor y Reconocimientos

**Desarrollado por:** Cristopher Luna 

Este proyecto fue desarrollado como una iniciativa para aplicar patrones de diseño de software y principios de arquitectura en el campo de la visión por computadora.

---
