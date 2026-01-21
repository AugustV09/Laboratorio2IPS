import os
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

# Generar la señal con los periodos que se quieran
periodo = int(input("Ingrese la cantidad de períodos: "))
senial_periodos = np.tile(senial_periodo, periodo)

# Generar señal con ruido
senial_periodos_ruido = senial_periodos + 7 * np.random.randn(len(senial_periodos))

# Calcular y graficar correlaciones con códigos Gold de satélites 2, 8 y 16
satelites = [2, 8, 16]
correlaciones = []

for svnum in satelites:
    # Generar código Gold para el satélite
    codigo = octave.cacode(svnum)
    codigo = np.array(codigo).flatten()
    
    # Repetir el código Gold tantas veces como períodos tenga la señal
    codigo = np.tile(codigo, periodo)
    
    # Calcular correlación circular entre la señal período y el código Gold
    correlacion = correlfft(senial_periodos_ruido, codigo)
    
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
    axes[idx].set_title(f'Correlación ({periodo} periodos): Señal incógnita con Ruido vs Satélite {svnum} (Correlación máx = {correlacion_max:.2f})', 
                        fontsize=12, fontweight='bold')
    axes[idx].set_xlabel('m')
    axes[idx].set_ylabel('Correlación')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].legend(loc='upper left')

plt.tight_layout()
plt.show()