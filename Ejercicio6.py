import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from oct2py import octave
from correlfft import correlacion_circular_fft

# Agregar la ruta donde está cacode.m al path de Octave
ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
octave.addpath(ruta_archivos)

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

# Extraer el primer período (primeros 1023 elementos)
senial_periodo = senial_completa[:1023]

# Agregar ruido gaussiano: equivalente a xincn = xinc+7*randn(size(xinc)) en MATLAB
senial_periodo_ruido = senial_periodo + 7 * np.random.randn(len(senial_periodo))

# Graficar ambas señales para comparación
plt.figure(figsize=(12, 6))

# Subplot 1: Señal original
plt.subplot(2, 1, 1)
plt.plot(senial_periodo, 'b-', linewidth=1.5)
plt.title('Señal Original (sin ruido)', fontsize=12, fontweight='bold')
plt.xlabel('t')
plt.ylabel('Amplitud')
plt.grid(True, alpha=0.3)
plt.legend(['Señal original'], loc='upper right')

# Subplot 2: Señal con ruido
plt.subplot(2, 1, 2)
plt.plot(senial_periodo_ruido, 'r-', linewidth=1.5)
plt.title('Señal con Ruido', fontsize=12, fontweight='bold')
plt.xlabel('t')
plt.ylabel('Amplitud')
plt.grid(True, alpha=0.3)
plt.legend(['Señal con ruido'], loc='upper right')

plt.tight_layout()
plt.show()