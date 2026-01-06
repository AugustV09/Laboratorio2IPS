import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

import numpy as np
import matplotlib.pyplot as plt
from oct2py import octave
from correlfft import correlacion_circular_fft

# Agregar la ruta donde está cacode.m al path de Octave
ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
octave.addpath(ruta_archivos)

# Ejecutar cacode(12) usando Octave
x = octave.cacode(12) #codigo Gold correspondiente al satelite 12
# Convertir a array de numpy
x = np.array(x).flatten()

# y será x pero desplzada 200 muestras hacia la derecha
y = np.roll(x, 200)

# Calcular intercorrelación de x e y
intercorr_xy = correlacion_circular_fft(x, y)

plt.figure(figsize=(12, 6))
plt.plot(intercorr_xy, 'g-', linewidth=1.5, alpha=0.7)
plt.title('Intercorrelación x-y')
plt.xlabel('n')
plt.ylabel('Correlación')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()