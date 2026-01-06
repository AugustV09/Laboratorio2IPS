import numpy as np


def correlacion_circular_fft(x, y):
    """
    Calcula la correlación circular de dos señales usando FFT.
    
    La correlación circular se calcula como:
    r = IFFT(FFT(x) * conj(FFT(y)))
    
    Parámetros:
    -----------
    x : array_like
        Primera señal de entrada
    y : array_like
        Segunda señal de entrada
    
    Retorna:
    --------
    numpy.ndarray
        Parte real de la correlación circular entre x e y
    """
    # Convertir a arrays de numpy
    x = np.asarray(x)
    y = np.asarray(y)
    
    # Asegurar que ambas señales tengan la misma longitud
    # Si tienen longitudes diferentes, se ajustan al máximo
    max_len = max(len(x), len(y))
    if len(x) < max_len:
        x = np.pad(x, (0, max_len - len(x)), mode='constant')
    if len(y) < max_len:
        y = np.pad(y, (0, max_len - len(y)), mode='constant')
    
    # Calcular FFT de ambas señales
    X = np.fft.fft(x)
    Y = np.fft.fft(y)
    
    # Calcular correlación circular: IFFT(FFT(x) * conj(FFT(y)))
    correlacion = np.fft.ifft(X * np.conj(Y))
    
    # Retornar la parte real
    return np.real(correlacion)

