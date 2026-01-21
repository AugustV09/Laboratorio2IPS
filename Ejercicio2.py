import os
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


# Generar señal aleatoria binaria del mismo tamaño que x
y = np.random.randint(0, 2, size=len(x))
# Convertir 0 a -1
y[y == 0] = -1

# Calcular autocorrelación de x
autocorr_x = correlfft(x, x)

# Calcular autocorrelación de y
autocorr_y = correlfft(y, y)

# Calcular intercorrelación de x e y
intercorr_xy = correlfft(x, y)

# Crear gráficos para comparar las 3 correlaciones
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

# Gráfico 1: Autocorrelación de x
axes[0].plot(autocorr_x, 'b-', linewidth=1.5)
axes[0].set_title('Autocorrelación de x (código Gold satélite 12)')
axes[0].set_xlabel('m')
axes[0].set_ylabel('Correlación')
axes[0].grid(True, alpha=0.3)

# Gráfico 2: Autocorrelación de y
axes[1].plot(autocorr_y, 'r-', linewidth=1.5)
axes[1].set_title('Autocorrelación de y')
axes[1].set_xlabel('m')
axes[1].set_ylabel('Correlación')
axes[1].grid(True, alpha=0.3)

# Gráfico 3: Intercorrelación de x e y
axes[2].plot(intercorr_xy, 'g-', linewidth=1.5)
axes[2].set_title('Intercorrelación de x e y')
axes[2].set_xlabel('m')
axes[2].set_ylabel('Correlación')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Longitud de x: {len(x)}")
print(f"Longitud de y: {len(y)}")
print(f"Valor máximo autocorrelación x: {np.max(autocorr_x):.2f}")
print(f"Valor máximo autocorrelación y: {np.max(autocorr_y):.2f}")
print(f"Valor máximo intercorrelación x-y: {np.max(intercorr_xy):.2f}")

