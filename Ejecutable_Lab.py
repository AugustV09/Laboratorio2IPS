import os
import subprocess
import sys

def mostrar_menu():
    """Muestra el menú de ejercicios disponibles"""
    print("\n" + "="*50)
    print("         MENÚ DE EJERCICIOS - LABORATORIO 2")
    print("="*50)
    print("  2. Ejecutar Ejercicio 2")
    print("  3. Ejecutar Ejercicio 3")
    print("  4. Ejecutar Ejercicio 4")
    print("  5. Ejecutar Ejercicio 5")
    print("  6. Ejecutar Ejercicio 6")
    print("  7. Ejecutar Ejercicio 7")
    print("  0. Salir")
    print("="*50)

def ejecutar_ejercicio(numero):
    """Ejecuta el ejercicio especificado por número"""
    nombre_archivo = f"Ejercicio{numero}.py"
    
    # Verificar que el archivo existe
    if not os.path.exists(nombre_archivo):
        print(f"\n❌ Error: No se encontró el archivo {nombre_archivo}")
        return
    
    print(f"\n🔄 Ejecutando {nombre_archivo}...")
    print("-"*50)
    
    try:
        # Ejecutar el script usando el intérprete de Python actual
        resultado = subprocess.run(
            [sys.executable, nombre_archivo],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            check=False  # No lanzar excepción si hay error, solo capturar código de salida
        )
        
        print("-"*50)
        if resultado.returncode == 0:
            print(f"✅ {nombre_archivo} ejecutado correctamente")
        else:
            print(f"⚠️  {nombre_archivo} finalizó con código de error: {resultado.returncode}")
            
    except Exception as e:
        print(f"❌ Error al ejecutar {nombre_archivo}: {str(e)}")

def main():
    """Función principal que maneja el menú interactivo"""
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (0-7): ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Hasta luego!")
                break
            elif opcion in ["2", "3", "4", "5", "6", "7"]:
                ejecutar_ejercicio(int(opcion))
                input("\nPresione Enter para continuar...")
            else:
                print("\n❌ Opción inválida. Por favor, seleccione una opción entre 0 y 7.")
                input("Presione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario. ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {str(e)}")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()
