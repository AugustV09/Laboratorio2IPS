import os

os.environ["OCTAVE_EXECUTABLE"] = (
    r"D:\Octavio\GNU Octave\Octave-10.3.0\mingw64\bin\octave-cli.exe"
)

import numpy as np
import matplotlib.pyplot as plt
from oct2py import octave
from correlfft import correlacion_circular_fft
from obtener_señal import obtener_senial_periodo

# Agregar la ruta donde está cacode.m al path de Octave
ruta_archivos = os.path.join(os.path.dirname(__file__), 'Archivos_PU2a')
octave.addpath(ruta_archivos)

# Cargar la señal incógnita desde el archivo .mat (un periodo)
senial_periodo = obtener_senial_periodo()

# # Generar señal con ruido
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

# Calcular y graficar correlaciones con códigos Gold de satélites 2, 8 y 16
satelites = [2, 8, 16]
correlaciones = []

for svnum in satelites:
    # Generar código Gold para el satélite
    codigo = octave.cacode(svnum)
    codigo = np.array(codigo).flatten()
    
    # Calcular correlación circular entre la señal período y el código Gold
    correlacion = correlacion_circular_fft(senial_periodo_ruido, codigo)
    
    # Encontrar el retardo y valor máximo
    retardo_max = np.argmax(correlacion)
    correlacion_max = np.max(correlacion)
    
    correlaciones.append({
        'satelite': svnum,
        'correlacion': correlacion,
        'retardo': retardo_max,
        'correlacion_max': correlacion_max
    })
    
    print(f"Satélite {svnum}: correlación máxima = {correlacion_max:.2f} en retardo {retardo_max}")

# Graficar las correlaciones
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

for idx, corr_data in enumerate(correlaciones):
    svnum = corr_data['satelite']
    correlacion = corr_data['correlacion']
    retardo = corr_data['retardo']
    correlacion_max = corr_data['correlacion_max']
    
    # Crear array de retardos
    retardos = np.arange(len(correlacion))
    
    axes[idx].plot(retardos, correlacion, 'b-', linewidth=1.5)
    # Marcar el pico máximo
    axes[idx].axvline(x=retardo, 
                      color='r', linestyle='--', linewidth=1.5, 
                      alpha=0.5, label=f"Retardo = {retardo}")
    axes[idx].set_title(f'Correlación: Señal período con Ruido vs Satélite {svnum} (Correlación máx = {correlacion_max:.2f})', 
                        fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('m')
    axes[idx].set_ylabel('Correlación')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].legend(loc='upper left')

plt.tight_layout()
plt.show()