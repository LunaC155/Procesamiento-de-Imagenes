import tkinter as tk
from tkinter import simpledialog, filedialog, colorchooser, messagebox
import cv2
import numpy as np
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import configuracion.estilos as estilos

# --- IMPORTACIONES DE TODOS LOS MÓDULOS ---
import configuracion.configuracion as config
import modulos.utilidades.carga_guardado as utils
import modulos.utilidades.visualizacion as visual
import modulos.utilidades.histogramas as f_hist
import modulos.utilidades.metricas as f_metricas
import modulos.utilidades.herramientas_dibujo as f_dibujo

import modulos.filtros.filtros_suavizado as f_suavizado
import modulos.filtros.filtros_bordes as f_bordes
import modulos.filtros.filtros_realce as f_realce
import modulos.filtros.filtros_morfologicos as f_morfo
import modulos.filtros.filtros_convolucion as f_conv

import modulos.color.conversion_color as f_color
import modulos.color.ajuste_color as f_ajuste_color
import modulos.color.ecualizacion as f_ecualizacion

import modulos.geometricas.transformaciones_basicas as f_geo
import modulos.geometricas.transformaciones_avanzadas as f_geo_av
import modulos.geometricas.recorte as f_recorte

import modulos.transformadas.transformada_fourier as f_fourier
import modulos.transformadas.transformada_hough as f_hough
import modulos.transformadas.transformada_coseno as f_dct
import modulos.transformadas.transformada_walsh as f_walsh

import modulos.segmentacion.umbralizacion as f_umbral
import modulos.segmentacion.segmentacion_regiones as f_regiones
import modulos.segmentacion.clustering as f_clustering

import modulos.compresion.compresion_perdida as f_comp_lossy
import modulos.compresion.metricas_compresion as f_comp_metrics

class ProcesadorImagenesApp:
    def __init__(self, root):
        # Configuración de ventana principal con Tema Moderno
        self.root = root
        self.style = ttk.Style(theme=estilos.TEMA_PREDEFINIDO)
        self.root.title(f"{config.APP_NOMBRE} - Studio Edition")
        self.root.geometry("1280x850")
        
        # --- ESTADO ---
        self.imagen_original = None 
        self.imagen_actual = None
        self.imagen_mostrada = None
        
        # Estado de Dibujo
        self.modo_dibujo = None 
        self.color_dibujo = (255, 0, 0)
        self.grosor_dibujo = 2
        self.inicio_mouse = None
        self.dibujando = False
        self.cache_dibujo = None # Para doble buffer (previsualización)

        # --- SISTEMA DE HISTORIAL ---
        self.historial = [] 
        self.indice_historial = -1

        # --- LAYOUT PRINCIPAL ---
        self._crear_menu_superior()
        self._crear_layout_principal()

        # --- ATAJOS DE TECLADO ---
        self.root.bind("<Control-z>", self.deshacer)
        self.root.bind("<Control-y>", self.rehacer)
        
    def _crear_layout_principal(self):
        """Divide la ventana en Barra de Estado, Panel Lateral y Área de Trabajo"""
        
        # 1. Barra de Estado (Abajo)
        self.barra_estado = ttk.Label(self.root, text="Listo. Carga una imagen para comenzar.", bootstyle=estilos.STYLE_ESTADO_NORMAL, padding=5)
        self.barra_estado.pack(side=BOTTOM, fill=X)

        # 2. Contenedor PanedWindow
        self.panel_dividido = ttk.Panedwindow(self.root, orient=HORIZONTAL)
        self.panel_dividido.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # 3. Panel Lateral (Izquierda)
        self.frame_lateral = ttk.Frame(self.panel_dividido, padding=10, width=250)
        self.panel_dividido.add(self.frame_lateral, weight=1)

        # 4. Área de Imagen (Derecha)
        self.frame_imagen = ttk.Frame(self.panel_dividido, padding=10)
        self.panel_dividido.add(self.frame_imagen, weight=4) 
        
        # Llenar los paneles
        self._llenar_panel_lateral()
        self._llenar_area_imagen()

    def _llenar_panel_lateral(self):
        """Crea pestañas de herramientas rápidas"""
        tabs = ttk.Notebook(self.frame_lateral)
        tabs.pack(fill=BOTH, expand=True)

        # Pestaña 1: Dibujo
        tab_dibujo = ttk.Frame(tabs, padding=10)
        tabs.add(tab_dibujo, text="🎨 Dibujo")
        self._construir_herramientas_dibujo(tab_dibujo)

        # Pestaña 2: Ajustes Rápidos
        tab_ajustes = ttk.Frame(tabs, padding=10)
        tabs.add(tab_ajustes, text="⚡ Ajustes")
        self._construir_ajustes_rapidos(tab_ajustes)

        # Pestaña 3: Info
        tab_info = ttk.Frame(tabs, padding=10)
        tabs.add(tab_info, text="ℹ️ Info")
        self.lbl_info_img = ttk.Label(tab_info, text="Sin imagen cargada", justify="left")
        self.lbl_info_img.pack(anchor="nw")

    def _construir_herramientas_dibujo(self, parent):
        ttk.Label(parent, text="Herramientas", font=estilos.FUENTE_TITULO).pack(pady=5)
        
        # Grid de botones
        grid_frame = ttk.Frame(parent)
        grid_frame.pack(fill=X)
        
        ttk.Button(grid_frame, text="✋ Mover", command=lambda: self._set_modo_dibujo(None), bootstyle=estilos.STYLE_BTN_ACCION).pack(fill=X, pady=2)
        ttk.Button(grid_frame, text="⬜ Rectángulo", command=lambda: self._set_modo_dibujo('rect'), bootstyle=estilos.STYLE_BTN_HERRAMIENTA).pack(fill=X, pady=2)
        ttk.Button(grid_frame, text="⭕ Círculo", command=lambda: self._set_modo_dibujo('circulo'), bootstyle=estilos.STYLE_BTN_HERRAMIENTA).pack(fill=X, pady=2)
        ttk.Button(grid_frame, text="✏️ Lápiz", command=lambda: self._set_modo_dibujo('lapiz'), bootstyle=estilos.STYLE_BTN_HERRAMIENTA).pack(fill=X, pady=2)
        ttk.Button(grid_frame, text="🔤 Texto", command=lambda: self._set_modo_dibujo('texto'), bootstyle=estilos.STYLE_BTN_HERRAMIENTA).pack(fill=X, pady=2)
        ttk.Button(grid_frame, text="🪣 Relleno", command=lambda: self._set_modo_dibujo('relleno'), bootstyle=estilos.STYLE_BTN_HERRAMIENTA).pack(fill=X, pady=2)
        
        ttk.Separator(parent, orient=HORIZONTAL).pack(fill=X, pady=10)
        
        ttk.Button(parent, text="🎨 Elegir Color", command=self._elegir_color, bootstyle=estilos.STYLE_BTN_COLOR).pack(fill=X)
        self.lbl_modo_actual = ttk.Label(parent, text="Modo: Navegar", font=estilos.FUENTE_PEQUENA, foreground="gray")
        self.lbl_modo_actual.pack(pady=10)

    def _construir_ajustes_rapidos(self, parent):
        ttk.Label(parent, text="Historial", font=estilos.FUENTE_TITULO).pack(pady=5)
        
        # Frame para botones de historial
        frame_hist = ttk.Frame(parent)
        frame_hist.pack(fill=X, pady=2)
        
        self.btn_deshacer = ttk.Button(frame_hist, text="↩ Deshacer", command=self.deshacer, bootstyle="secondary", state=DISABLED)
        self.btn_deshacer.pack(side=LEFT, fill=X, expand=True, padx=2)
        
        self.btn_rehacer = ttk.Button(frame_hist, text="↪ Rehacer", command=self.rehacer, bootstyle="secondary", state=DISABLED)
        self.btn_rehacer.pack(side=RIGHT, fill=X, expand=True, padx=2)

        ttk.Separator(parent, orient=HORIZONTAL).pack(fill=X, pady=10)

        ttk.Label(parent, text="Filtros Comunes", font=estilos.FUENTE_TITULO).pack(pady=5)
        
        ttk.Button(parent, text="Grises", command=lambda: self.aplicar_filtro(f_color.a_escala_grises)).pack(fill=X, pady=2)
        ttk.Button(parent, text="Suavizado", command=lambda: self.aplicar_filtro(f_suavizado.aplicar_gaussiano)).pack(fill=X, pady=2)
        ttk.Button(parent, text="Bordes Canny", command=lambda: self.aplicar_filtro(f_bordes.aplicar_canny)).pack(fill=X, pady=2)
        ttk.Button(parent, text="Ecualizar", command=lambda: self.aplicar_filtro(f_ecualizacion.ecualizar_histograma)).pack(fill=X, pady=2)
        
        ttk.Separator(parent, orient=HORIZONTAL).pack(fill=X, pady=10)
        ttk.Label(parent, text="Acciones", font=estilos.FUENTE_TITULO).pack(pady=5)
        
        ttk.Button(parent, text="Original", command=self.restaurar_original, bootstyle=estilos.STYLE_BTN_PELIGRO).pack(fill=X, pady=2)
        ttk.Button(parent, text="Histograma", command=lambda: f_hist.mostrar_histograma(self.imagen_actual), bootstyle=estilos.STYLE_BTN_EXITO).pack(fill=X, pady=2)

    def _llenar_area_imagen(self):
        contenedor = ttk.Labelframe(self.frame_imagen, text="Vista Previa", padding=0)
        contenedor.pack(fill=BOTH, expand=True)
        
        self.lbl_imagen = ttk.Label(contenedor, text="📂\nArrastra o abre una imagen", anchor="center")
        self.lbl_imagen.pack(fill=BOTH, expand=True)

        self.lbl_imagen.bind("<Button-1>", self._al_presionar_mouse)
        self.lbl_imagen.bind("<B1-Motion>", self._al_arrastrar_mouse)
        self.lbl_imagen.bind("<ButtonRelease-1>", self._al_soltar_mouse)
        self.lbl_imagen.bind("<Motion>", self._actualizar_status_mouse)

    # ==========================================
    #           SISTEMA DE HISTORIAL
    # ==========================================
    def _registrar_cambio(self):
        """Guarda el estado actual en el historial."""
        if self.imagen_actual is None: return

        # Si estamos en medio del historial y hacemos un cambio, borramos el futuro
        if self.indice_historial < len(self.historial) - 1:
            self.historial = self.historial[:self.indice_historial+1]
        
        # Guardamos copia
        self.historial.append(self.imagen_actual.copy())
        self.indice_historial += 1
        
        # Limitar memoria (últimos 20 pasos)
        if len(self.historial) > 20:
            self.historial.pop(0)
            self.indice_historial -= 1

        self._actualizar_estado_botones_historial()

    def deshacer(self, event=None):
        if self.indice_historial > 0:
            self.indice_historial -= 1
            self.imagen_actual = self.historial[self.indice_historial].copy()
            self._actualizar_vista()
            self.barra_estado.config(text="Deshacer realizado", bootstyle="info")
            self._actualizar_estado_botones_historial()

    def rehacer(self, event=None):
        if self.indice_historial < len(self.historial) - 1:
            self.indice_historial += 1
            self.imagen_actual = self.historial[self.indice_historial].copy()
            self._actualizar_vista()
            self.barra_estado.config(text="Rehacer realizado", bootstyle="info")
            self._actualizar_estado_botones_historial()

    def _actualizar_estado_botones_historial(self):
        state_undo = NORMAL if self.indice_historial > 0 else DISABLED
        self.btn_deshacer.config(state=state_undo)
        
        state_redo = NORMAL if self.indice_historial < len(self.historial) - 1 else DISABLED
        self.btn_rehacer.config(state=state_redo)

    # ==========================================
    #           MENÚ SUPERIOR
    # ==========================================
    def _crear_menu_superior(self):
        barra_menu = tk.Menu(self.root)
        self.root.config(menu=barra_menu)

        # MENÚ ARCHIVO
        m_archivo = tk.Menu(barra_menu, tearoff=0)
        m_archivo.add_command(label="📂 Cargar Imagen", command=self.cargar_imagen)
        m_archivo.add_command(label="💾 Guardar Resultado", command=self.guardar_resultado)
        m_archivo.add_separator()
        m_archivo.add_command(label="❌ Salir", command=self.root.quit)
        barra_menu.add_cascade(label="Archivo", menu=m_archivo)

        # MENÚ FILTROS
        m_filtros = tk.Menu(barra_menu, tearoff=0)
        
        m_suav = tk.Menu(m_filtros, tearoff=0)
        m_suav.add_command(label="Promedio", command=lambda: self.aplicar_filtro(f_suavizado.aplicar_promedio))
        m_suav.add_command(label="Gaussiano", command=lambda: self.aplicar_filtro(f_suavizado.aplicar_gaussiano))
        m_suav.add_command(label="Mediana", command=lambda: self.aplicar_filtro(f_suavizado.aplicar_mediana))
        m_suav.add_command(label="Bilateral", command=lambda: self.aplicar_filtro(f_suavizado.aplicar_bilateral))
        m_filtros.add_cascade(label="Suavizado", menu=m_suav)

        m_realce = tk.Menu(m_filtros, tearoff=0)
        m_realce.add_command(label="Sharpen", command=lambda: self.aplicar_filtro(f_realce.aplicar_sharpen))
        m_realce.add_command(label="Paso Alto", command=lambda: self.aplicar_filtro(f_realce.aplicar_paso_alto))
        m_realce.add_command(label="Unsharp Mask", command=lambda: self.aplicar_filtro(f_realce.unsharp_mask))
        m_filtros.add_cascade(label="Realce", menu=m_realce)

        m_bordes = tk.Menu(m_filtros, tearoff=0)
        m_bordes.add_command(label="Sobel", command=lambda: self.aplicar_filtro(f_bordes.aplicar_sobel))
        m_bordes.add_command(label="Canny", command=lambda: self.aplicar_filtro(f_bordes.aplicar_canny))
        m_bordes.add_command(label="Laplaciano", command=lambda: self.aplicar_filtro(f_bordes.aplicar_laplaciano))
        m_bordes.add_command(label="Prewitt", command=lambda: self.aplicar_filtro(f_bordes.aplicar_prewitt))
        m_filtros.add_cascade(label="Bordes", menu=m_bordes)

        m_morfo = tk.Menu(m_filtros, tearoff=0)
        m_morfo.add_command(label="Erosión", command=lambda: self.aplicar_filtro(f_morfo.erosion))
        m_morfo.add_command(label="Dilatación", command=lambda: self.aplicar_filtro(f_morfo.dilatacion))
        m_morfo.add_command(label="Apertura", command=lambda: self.aplicar_filtro(f_morfo.apertura))
        m_morfo.add_command(label="Cierre", command=lambda: self.aplicar_filtro(f_morfo.cierre))
        m_morfo.add_command(label="Top Hat", command=lambda: self.aplicar_filtro(f_morfo.top_hat))
        m_morfo.add_command(label="Black Hat", command=lambda: self.aplicar_filtro(f_morfo.black_hat))
        m_morfo.add_command(label="Gradiente", command=lambda: self.aplicar_filtro(f_morfo.gradiente_morfologico))
        m_filtros.add_cascade(label="Morfológicos", menu=m_morfo)

        m_conv = tk.Menu(m_filtros, tearoff=0)
        m_conv.add_command(label="Emboss", command=lambda: self.aplicar_filtro(f_conv.aplicar_emboss))
        m_filtros.add_cascade(label="Artísticos", menu=m_conv)

        barra_menu.add_cascade(label="Filtros", menu=m_filtros)

        # MENÚ TRANSFORMADAS
        m_trans = tk.Menu(barra_menu, tearoff=0)
        m_trans.add_command(label="Fourier (Espectro)", command=lambda: self.aplicar_filtro(f_fourier.obtener_espectro))
        m_trans.add_command(label="Coseno (DCT)", command=lambda: self.aplicar_filtro(f_dct.aplicar_dct))
        m_trans.add_command(label="Walsh-Hadamard", command=lambda: self.aplicar_filtro(f_walsh.aplicar_walsh_hadamard))
        m_trans.add_separator()
        m_trans.add_command(label="Hough (Líneas)", command=lambda: self.aplicar_filtro(f_hough.detectar_lineas))
        m_trans.add_command(label="Hough (Círculos)", command=lambda: self.aplicar_filtro(f_hough.detectar_circulos))
        barra_menu.add_cascade(label="Transformadas", menu=m_trans)

        # MENÚ COLOR
        m_color = tk.Menu(barra_menu, tearoff=0)
        m_color.add_command(label="Escala de Grises", command=lambda: self.aplicar_filtro(f_color.a_escala_grises))
        m_color.add_command(label="Ecualizar Histograma", command=lambda: self.aplicar_filtro(f_ecualizacion.ecualizar_histograma))
        m_color.add_separator()
        m_color.add_command(label="Brillo/Contraste...", command=self._pedir_brillo_contraste)
        m_color.add_command(label="Saturación...", command=self._pedir_saturacion)
        barra_menu.add_cascade(label="Color", menu=m_color)

        # MENÚ GEOMETRÍA
        m_geo = tk.Menu(barra_menu, tearoff=0)
        m_geo.add_command(label="Rotar...", command=self._pedir_rotacion)
        m_geo.add_command(label="Escalar...", command=self._pedir_escalado)
        m_geo.add_command(label="Traslación...", command=self._pedir_traslacion)
        m_geo.add_separator()
        m_geo.add_command(label="Flip Horizontal", command=lambda: self.aplicar_filtro(f_geo.voltear_imagen, codigo=1))
        m_geo.add_command(label="Flip Vertical", command=lambda: self.aplicar_filtro(f_geo.voltear_imagen, codigo=0))
        m_geo.add_separator()
        m_geo.add_command(label="Shear (Sesgado)", command=lambda: self.aplicar_filtro(f_geo_av.aplicar_sesgado))
        m_geo.add_command(label="Perspectiva (Demo)", command=lambda: self.aplicar_filtro(f_geo_av.correccion_perspectiva_demo))
        barra_menu.add_cascade(label="Geometría", menu=m_geo)

        # MENÚ SEGMENTACIÓN
        m_seg = tk.Menu(barra_menu, tearoff=0)
        m_seg.add_command(label="Umbral Otsu", command=lambda: self.aplicar_filtro(f_umbral.umbral_otsu))
        m_seg.add_command(label="Umbral Adaptativo", command=lambda: self.aplicar_filtro(f_umbral.umbral_adaptativo))
        m_seg.add_command(label="Watershed", command=lambda: self.aplicar_filtro(f_regiones.aplicar_watershed))
        m_seg.add_command(label="K-Means...", command=self._pedir_kmeans)
        barra_menu.add_cascade(label="Segmentación", menu=m_seg)

        # MENÚ COMPRESIÓN
        m_comp = tk.Menu(barra_menu, tearoff=0)
        m_comp.add_command(label="Simular JPEG (Q=10)", command=lambda: self.aplicar_filtro(f_comp_lossy.simular_jpeg, calidad=10))
        m_comp.add_command(label="Info Compresión", command=self._mostrar_info_compresion)
        barra_menu.add_cascade(label="Compresión", menu=m_comp)

        # MENÚ ANÁLISIS
        m_her = tk.Menu(barra_menu, tearoff=0)
        m_her.add_command(label="Histograma", command=lambda: f_hist.mostrar_histograma(self.imagen_actual))
        m_her.add_command(label="Comparar Lado a Lado", command=self.abrir_comparacion)
        m_her.add_command(label="Métricas (PSNR/MSE)", command=self._calcular_metricas)
        barra_menu.add_cascade(label="Análisis", menu=m_her)

    # ==========================================
    #           LÓGICA DEL MOUSE Y DIBUJO
    # ==========================================
    def _set_modo_dibujo(self, modo):
        self.modo_dibujo = modo
        texto = f"Modo: {modo.upper()}" if modo else "Modo: NAVEGAR"
        estilo = "inverse-danger" if modo else "inverse-secondary"
        
        self.lbl_modo_actual.config(text=texto)
        self.barra_estado.config(text=f"Herramienta seleccionada: {texto}", bootstyle=estilo)
        
        # CAMBIO DE CURSOR
        cursores = {
            'rect': 'crosshair', 
            'circulo': 'crosshair', 
            'lapiz': 'pencil', 
            'texto': 'ibeam', 
            'relleno': 'spider', 
            None: 'arrow'
        }
        cursor_actual = cursores.get(modo, 'arrow')
        self.lbl_imagen.config(cursor=cursor_actual)

    def _actualizar_status_mouse(self, event):
        x, y = self._obtener_coords_imagen(event.x, event.y)
        if x is not None and self.imagen_actual is not None:
            h, w = self.imagen_actual.shape[:2]
            if 0 <= x < w and 0 <= y < h:
                if len(self.imagen_actual.shape) == 3:
                    pixel = self.imagen_actual[y, x]
                    txt_color = f"RGB{tuple(pixel)}"
                else:
                    pixel = self.imagen_actual[y, x]
                    txt_color = f"Gris: {pixel}"
                
                self.barra_estado.config(text=f"X: {x}, Y: {y} | {txt_color}")
        else:
            self.barra_estado.config(text="Fuera de imagen")

    def _elegir_color(self):
        color = colorchooser.askcolor(title="Color de dibujo")[0]
        if color:
            self.color_dibujo = tuple(map(int, color))

    def _al_presionar_mouse(self, event):
        if not self.modo_dibujo or self.imagen_actual is None: return
        x, y = self._obtener_coords_imagen(event.x, event.y)
        if x is None: return

        self.inicio_mouse = (x, y)
        self.dibujando = True
        
        # Guardar estado limpio para previsualización (Doble Buffer)
        self.cache_dibujo = self.imagen_actual.copy()

        if self.modo_dibujo == 'texto':
            texto = simpledialog.askstring("Texto", "Ingresa el texto:")
            if texto:
                self.aplicar_filtro(f_dibujo.escribir_texto, texto=texto, x=x, y=y, color=self.color_dibujo)
            self.dibujando = False
            self.cache_dibujo = None
            
        elif self.modo_dibujo == 'relleno':
            self.aplicar_filtro(f_dibujo.relleno_floodfill, x=x, y=y, color_nuevo=self.color_dibujo)
            self.dibujando = False
            self.cache_dibujo = None
            
    def _al_arrastrar_mouse(self, event):
        if not self.dibujando: return
        
        x, y = self._obtener_coords_imagen(event.x, event.y)
        if x is None: return
        ini_x, ini_y = self.inicio_mouse

        # CASO 1: LÁPIZ (Dibujo directo permanente)
        if self.modo_dibujo == 'lapiz':
            self.imagen_actual = f_dibujo.dibujar_circulo(self.imagen_actual, x, y, self.grosor_dibujo, self.color_dibujo, -1)
            self._actualizar_vista()
            
        # CASO 2: FORMAS (Previsualización con cache)
        elif self.modo_dibujo in ['rect', 'circulo']:
            # Tomamos la imagen LIMPIA
            img_temp = self.cache_dibujo.copy()
            
            if self.modo_dibujo == 'rect':
                w, h = abs(x - ini_x), abs(y - ini_y)
                ix, iy = min(ini_x, x), min(ini_y, y)
                img_temp = f_dibujo.dibujar_rectangulo(img_temp, ix, iy, w, h, self.color_dibujo, self.grosor_dibujo)
            
            elif self.modo_dibujo == 'circulo':
                radio = int(np.sqrt((x - ini_x)**2 + (y - ini_y)**2))
                img_temp = f_dibujo.dibujar_circulo(img_temp, ini_x, ini_y, radio, self.color_dibujo, self.grosor_dibujo)
            
            # Solo mostramos, NO guardamos
            self.imagen_mostrada = visual.convertir_a_tk(img_temp, ancho_max=1000, alto_max=700)
            self.lbl_imagen.configure(image=self.imagen_mostrada)
            
    def _al_soltar_mouse(self, event):
        if not self.dibujando or not self.inicio_mouse: return
        self.dibujando = False
        
        fin_x, fin_y = self._obtener_coords_imagen(event.x, event.y)
        if fin_x is None: 
            self._actualizar_vista()
            return
            
        ini_x, ini_y = self.inicio_mouse

        # Si es lápiz, el dibujo ya está hecho, solo registramos historial
        if self.modo_dibujo == 'lapiz':
             self._registrar_cambio()

        # Si es forma, aplicamos el cambio definitivo
        elif self.modo_dibujo == 'rect':
            w, h = abs(fin_x - ini_x), abs(fin_y - ini_y)
            x, y = min(ini_x, fin_x), min(ini_y, fin_y)
            self.aplicar_filtro(f_dibujo.dibujar_rectangulo, x=x, y=y, w=w, h=h, color=self.color_dibujo, grosor=self.grosor_dibujo)
        
        elif self.modo_dibujo == 'circulo':
            radio = int(np.sqrt((fin_x - ini_x)**2 + (fin_y - ini_y)**2))
            self.aplicar_filtro(f_dibujo.dibujar_circulo, centro_x=ini_x, centro_y=ini_y, radio=radio, color=self.color_dibujo, grosor=self.grosor_dibujo)
        
        self.cache_dibujo = None

    def _obtener_coords_imagen(self, gui_x, gui_y):
        if self.imagen_mostrada is None: return None, None
        img_w, img_h = self.imagen_mostrada.width(), self.imagen_mostrada.height()
        widget_w, widget_h = self.lbl_imagen.winfo_width(), self.lbl_imagen.winfo_height()
        
        offset_x, offset_y = (widget_w - img_w) // 2, (widget_h - img_h) // 2
        rel_x, rel_y = gui_x - offset_x, gui_y - offset_y

        if rel_x < 0 or rel_x >= img_w or rel_y < 0 or rel_y >= img_h: return None, None

        orig_h, orig_w = self.imagen_actual.shape[:2]
        scale_x, scale_y = orig_w / img_w, orig_h / img_h
        return int(rel_x * scale_x), int(rel_y * scale_y)

    # ==========================================
    #           MÉTODOS AUXILIARES
    # ==========================================
    def cargar_imagen(self):
        img_rgb, ruta = utils.cargar_imagen_dialogo()
        if img_rgb is not None:
            self.imagen_original = img_rgb.copy()
            self.imagen_actual = img_rgb.copy()
            
            # Reiniciar historial
            self.historial = []
            self.indice_historial = -1
            self._registrar_cambio()

            self._actualizar_vista()
            
            h, w = self.imagen_actual.shape[:2]
            canales = 3 if len(self.imagen_actual.shape) == 3 else 1
            info = f"Dim: {w}x{h}\nCanales: {canales}\nRuta: ...{ruta[-20:]}"
            self.lbl_info_img.config(text=info)
            self.barra_estado.config(text=f"Imagen cargada: {ruta}", bootstyle=estilos.STYLE_ESTADO_EXITO)

    def guardar_resultado(self):
        if self.imagen_actual is not None:
            if utils.guardar_imagen_dialogo(self.imagen_actual):
                messagebox.showinfo("Éxito", "Imagen guardada correctamente.")

    def restaurar_original(self):
        if self.imagen_original is not None:
            self.imagen_actual = self.imagen_original.copy()
            self._registrar_cambio() # Guardamos la restauración como un paso nuevo
            self._actualizar_vista()
            self.barra_estado.config(text="Imagen restaurada a original", bootstyle=estilos.STYLE_ESTADO_NORMAL)

    def aplicar_filtro(self, funcion_filtro, **kwargs):
        if self.imagen_actual is not None:
            try:
                self.barra_estado.config(text="Procesando...", bootstyle=estilos.STYLE_ESTADO_PROCESANDO)
                self.root.update() 
                
                res = funcion_filtro(self.imagen_actual, **kwargs)
                if res is not None:
                    self.imagen_actual = res
                    self._actualizar_vista()
                    
                    # Guardamos en historial
                    self._registrar_cambio()
                    
                    self.barra_estado.config(text="Filtro aplicado con éxito", bootstyle=estilos.STYLE_ESTADO_EXITO)
            except Exception as e:
                print(e)
                messagebox.showerror("Error", f"Fallo al procesar: {str(e)}")
                self.barra_estado.config(text="Error al procesar", bootstyle=estilos.STYLE_ESTADO_ERROR)
        else:
            messagebox.showwarning("Atención", "Carga una imagen primero.")

    def _actualizar_vista(self):
        img_tk = visual.convertir_a_tk(self.imagen_actual, ancho_max=1000, alto_max=700)
        self.imagen_mostrada = img_tk
        self.lbl_imagen.configure(image=img_tk, text="")

    # --- DIÁLOGOS ---
    def _pedir_rotacion(self):
        val = simpledialog.askfloat("Rotar", "Grados:", minvalue=-360, maxvalue=360)
        if val: self.aplicar_filtro(f_geo.rotar_imagen, grados=val)
    def _pedir_escalado(self):
        val = simpledialog.askinteger("Escalar", "Porcentaje (%):", minvalue=1, maxvalue=500)
        if val: self.aplicar_filtro(f_geo.escalar_imagen, porcentaje=val)
    def _pedir_traslacion(self):
        x = simpledialog.askinteger("Traslación", "X (px):", minvalue=-500, maxvalue=500)
        y = simpledialog.askinteger("Traslación", "Y (px):", minvalue=-500, maxvalue=500)
        if x is not None and y is not None:
            self.aplicar_filtro(f_geo.traslacion, x=x, y=y)
    def _pedir_kmeans(self):
        k = simpledialog.askinteger("K-Means", "Clusters (K):", minvalue=2, maxvalue=20)
        if k: self.aplicar_filtro(f_clustering.segmentar_kmeans, k=k)
    def _pedir_brillo_contraste(self):
        b = simpledialog.askinteger("Brillo", "Valor (-100 a 100):", minvalue=-100, maxvalue=100)
        c = simpledialog.askinteger("Contraste", "Valor (-100 a 100):", minvalue=-100, maxvalue=100)
        if b is not None and c is not None:
            self.aplicar_filtro(f_ajuste_color.ajustar_brillo_contraste, brillo=b, contraste=c)
    def _pedir_saturacion(self):
        s = simpledialog.askfloat("Saturación", "Factor (0.0 a 3.0):", minvalue=0.0, maxvalue=3.0)
        if s is not None: self.aplicar_filtro(f_ajuste_color.ajustar_saturacion, incremento=s)
    def _mostrar_info_compresion(self):
        if self.imagen_actual is None: return
        kb, ratio = f_comp_metrics.calcular_tasa_compresion(self.imagen_actual, 10)
        messagebox.showinfo("Compresión", f"Tamaño estimado (JPG Q=10): {kb:.2f} KB\nRatio: {ratio:.2f}:1")
    def _calcular_metricas(self):
        if self.imagen_original is None: return
        psnr = f_metricas.calcular_psnr(self.imagen_original, self.imagen_actual)
        mse = f_metricas.calcular_mse(self.imagen_original, self.imagen_actual)
        messagebox.showinfo("Métricas", f"Comparando con Original:\nMSE: {mse:.2f}\nPSNR: {psnr:.2f} dB")
    def abrir_comparacion(self):
        if self.imagen_original is None: return
        ventana = ttk.Toplevel(self.root) 
        ventana.title("Comparación")
        ventana.geometry("1000x600")
        
        frame = ttk.Frame(ventana)
        frame.pack(fill=BOTH, expand=True)
        
        img1 = visual.convertir_a_tk(self.imagen_original, 480, 550)
        img2 = visual.convertir_a_tk(self.imagen_actual, 480, 550)
        
        lbl1 = ttk.Label(frame, image=img1, text="ORIGINAL", compound="bottom", font=estilos.FUENTE_COMPARACION)
        lbl1.image = img1
        lbl1.pack(side=LEFT, padx=10, expand=True)
        
        ttk.Separator(frame, orient=VERTICAL).pack(side=LEFT, fill=Y)
        
        lbl2 = ttk.Label(frame, image=img2, text="EDITADA", compound="bottom", font=estilos.FUENTE_COMPARACION)
        lbl2.image = img2
        lbl2.pack(side=RIGHT, padx=10, expand=True)