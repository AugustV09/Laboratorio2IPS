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

print(f"Longitud de la señal completa: {len(senial_completa)}")
print(f"Longitud del período extraído: {len(senial_periodo)}")

# Almacenar resultados de intercorrelación para todos los satélites
satelites_presentes = []

# Calcular intercorrelación para cada satélite (1 a 32)
print("\nCalculando intercorrelaciones para satélites 1-32...")
for svnum in range(1, 33):
    # Generar código Gold para el satélite svnum
    codigo = octave.cacode(svnum)
    codigo = np.array(codigo).flatten()
    
    # Calcular intercorrelación circular
    intercorr = correlacion_circular_fft(senial_periodo, codigo)
    
    # Almacenar resultados

    indice_max = np.argmax(intercorr)
    correlacion_max = np.max(intercorr)

    '''
            if indice_max > 511:
            retardo = indice_max - 1023
        else:
            retardo = indice_max
    '''

    satelites_presentes.append({
        'satelite': svnum,
        'intercorrelacion': intercorr,
        'retardo': indice_max,
        'indice': indice_max,
        'correlacion_max': correlacion_max
    })
    
    print(f"Satélite {svnum:2d}: máximo = {correlacion_max:8.2f} en índice {indice_max}")


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

for idx, sat in enumerate(top_3):
    svnum = sat['satelite']
    intercorr = sat['intercorrelacion']
    
    # Crear array de retardos
    retardos = np.arange(len(intercorr))
    
    axes[idx].plot(retardos, intercorr, 'b-', linewidth=1.5)
    # Marcar el pico máximo
    axes[idx].axvline(x=sat['indice'], 
                        color='r', linestyle='--', linewidth=2, 
                        label=f"Retardo = {sat['retardo']} (índice {sat['indice']})")
    axes[idx].set_title(f'Intercorrelación: Señal incógnita vs Satélite {svnum} (Correlación máx = {sat["correlacion_max"]:.2f})')
    axes[idx].set_xlabel('Retardo (muestras)')
    axes[idx].set_ylabel('Correlación')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].legend()

plt.tight_layout()
plt.show()


