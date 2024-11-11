from src.initApi import InitApi
import sys

# Crear la instancia de la aplicación Flask
app = InitApi.createInstanceApi()

if __name__ == "__main__":
    try:
        # Ejecutar la aplicación en modo debug
        app.run(debug=True)
    except Exception as e:
        # Manejo de errores de inicialización
        print("Error al iniciar la aplicación:", e)
        sys.exit(e)
