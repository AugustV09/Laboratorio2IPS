import os
from scipy.io import loadmat


def obtener_senial_periodo():
    """
    Recupera la señal completa de la señal incógnita
    desde el archivo senial_incognita.mat.
    
    Returns:
        numpy.ndarray: Array con la señal completa.
    """
    # Obtener la ruta del directorio actual
    ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
    
    # Cargar la señal incógnita desde el archivo .mat
    ruta_senial = os.path.join(ruta_archivos, 'senial_incognita.mat')
    datos = loadmat(ruta_senial)
    
    # Obtener la señal (puede tener diferentes nombres de variables en el .mat)
    # Buscar la clave que no sea '__header__', '__version__', '__globals__'
    claves = [k for k in datos.keys() if not k.startswith('__')]
    if len(claves) > 0:
        senial_completa = datos[claves[0]].flatten()
    else:
        raise ValueError("No se encontró la señal en el archivo .mat")
    
    return senial_completa[:1023]
