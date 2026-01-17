import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

import numpy as np
import matplotlib.pyplot as plt
from oct2py import octave
from Ejercicio1 import correlfft
from obtener_senial import obtener_senial_periodo

# Agregar la ruta donde está cacode.m al path de Octave
ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
octave.addpath(ruta_archivos)

# Cargar la señal incógnita desde el archivo .mat (un periodo)
senial_periodo = obtener_senial_periodo()

# Almacenar resultados de intercorrelación para todos los satélites
satelites_presentes = []

# Calcular intercorrelación para cada satélite (1 a 32)
print("\nCalculando intercorrelaciones para satélites 1-32...")
for svnum in range(1, 33):
    # Generar código Gold para el satélite svnum
    codigo = octave.cacode(svnum)
    codigo = np.array(codigo).flatten()
    
    # Calcular intercorrelación circular
    intercorr = correlfft(senial_periodo, codigo)
    # Desplazar el resultado de la intercorrelación 511 muestras a la derecha
    intercorr = np.roll(intercorr, 511)

    # Almacenar resultados

    retardo_max = np.argmax(intercorr) - 511
    correlacion_max = np.max(intercorr)

    satelites_presentes.append({
        'satelite': svnum,
        'intercorrelacion': intercorr,
        'retardo': retardo_max,
        'correlacion_max': correlacion_max
    })
    
    print(f"Satélite {svnum:2d}: máximo = {correlacion_max:8.2f} en índice {retardo_max}")


# Ordenar por correlación máxima (de mayor a menor)
satelites_presentes.sort(key=lambda x: x['correlacion_max'], reverse=True)

# Mostrar los 3 satélites con mayor correlación
print(f"\n{'='*60}")
print(f"Top 3 satélites con mayor correlación máxima:")
print(f"{'='*60}")
for i, sat in enumerate(satelites_presentes[:3], 1):
    print(f"{i}. Satélite {sat['satelite']:2d}: correlación máxima = {sat['correlacion_max']:8.2f}, retardo = {sat['retardo']:4d}")

# Graficar los 3 satélites con mayor correlación máxima
top_3 = satelites_presentes[:3]

fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# Crear array de retardos de -511 a 511
retardos = np.arange(-511, 512)

for idx, sat in enumerate(top_3):
    svnum = sat['satelite']
    intercorr = sat['intercorrelacion']
    
    axes[idx].plot(retardos, intercorr, 'b-', linewidth=1.5)
    # Marcar el pico máximo
    axes[idx].axvline(x=sat['retardo'], 
                        color='r', linestyle='--', linewidth=1.5, 
                        alpha=0.5, label=f"Retardo = {sat['retardo']}")
    axes[idx].set_title(f'Intercorrelación: Señal incógnita vs Satélite {svnum} (Correlación máx = {sat["correlacion_max"]:.2f})')
    axes[idx].set_xlabel('m')
    axes[idx].set_ylabel('Correlación')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].legend(loc='upper left')

plt.tight_layout()
plt.show()


