from src.initApi import InitApi
import sys
from flask_swagger_ui import get_swaggerui_blueprint

# Crear la instancia de la aplicación Flask
app = InitApi.createInstanceApi()


# Configuración de Swagger UI
SWAGGER_URL = '/swagger'  # URL donde estará la documentación
API_URL = '../static/swagger.yaml'  # Ruta del archivo YAML

# Configuración de Swagger UI Blueprint
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    try:
        # Ejecutar la aplicación en modo debug
        app.run(debug=True)
    except Exception as e:
        # Manejo de errores de inicialización
        print("Error al iniciar la aplicación:", e)
        sys.exit(e)
