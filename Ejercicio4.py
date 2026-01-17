import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

import numpy as np
import matplotlib.pyplot as plt
from oct2py import octave
from Ejercicio1 import correlfft

# Agregar la ruta donde está cacode.m al path de Octave
ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
octave.addpath(ruta_archivos)

# Ejecutar cacode(12) usando Octave
x = octave.cacode(12) #codigo Gold correspondiente al satelite 12
# Convertir a array de numpy
x = np.array(x).flatten()

# y será x pero desplzada 200 muestras hacia la derecha
y = np.roll(x, 200)

# Calcular intercorrelación de x con y
intercorr_xy = correlfft(x, y)
# Desplazar el resultado de la intercorrelación 511 muestras a la derecha
intercorr_xy = np.roll(intercorr_xy, 511)

# Calcular intercorrelación de y con x
intercorr_yx = correlfft(y, x)
# Desplazar el resultado de la intercorrelación 511 muestras a la derecha
intercorr_yx = np.roll(intercorr_yx, 511)

# Encontrar el índice del pico de correlación para x-y
indice_pico_xy = np.argmax(intercorr_xy) - 511
valor_pico_xy = intercorr_xy[indice_pico_xy]

# Encontrar el índice del pico de correlación para y-x
indice_pico_yx = np.argmax(intercorr_yx) - 511
valor_pico_yx = intercorr_yx[indice_pico_yx]

print(f"El pico de correlación x-y se encuentra en el retardo: {indice_pico_xy}")
print(f"El pico de correlación y-x se encuentra en el retardo: {indice_pico_yx}")

# Crear array de retardos de -511 a 511
retardos = np.arange(-511, 512)

# Crear figura con dos subgráficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Gráfico 1: Intercorrelación x-y
ax1.plot(retardos, intercorr_xy, 'g-', linewidth=1.5, alpha=0.7)
ax1.axvline(x=indice_pico_xy, color='r', linestyle='--', alpha=0.5, linewidth=1.5, label=f'Pico en m={indice_pico_xy}')
ax1.set_title('Intercorrelación x-y')
ax1.set_xlabel('m')
ax1.set_ylabel('Correlación')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Gráfico 2: Intercorrelación y-x
ax2.plot(retardos, intercorr_yx, 'g-', linewidth=1.5, alpha=0.7)
ax2.axvline(x=indice_pico_yx, color='r', linestyle='--', alpha=0.5, linewidth=1.5, label=f'Pico en m={indice_pico_yx}')
ax2.set_title('Intercorrelación y-x')
ax2.set_xlabel('m')
ax2.set_ylabel('Correlación')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()