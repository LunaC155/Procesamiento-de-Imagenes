def recorte_central(imagen, porcentaje=0.5):
    """
    Recorta el centro de la imagen.
    Args:
        porcentaje: Qué tanto de la imagen conservar (0.0 a 1.0).
                    0.5 mantiene el 50% central.
    """
    h, w = imagen.shape[:2]
    
    # Calcular nuevos tamaños
    nuevo_h = int(h * porcentaje)
    nuevo_w = int(w * porcentaje)
    
    # Calcular coordenadas de inicio (esquina superior izquierda del recorte)
    inicio_y = (h - nuevo_h) // 2
    inicio_x = (w - nuevo_w) // 2
    
    # Slicing de Numpy: imagen[y:y+h, x:x+w]
    return imagen[inicio_y:inicio_y+nuevo_h, inicio_x:inicio_x+nuevo_w]