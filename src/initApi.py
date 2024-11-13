from flask import Flask
from flask_cors import CORS

from src.api.apiAuth import api_auth

class InitApi:

    _instance = None

    def getApiInstance():
        if InitApi._instance is None:
            return InitApi
        return InitApi._instance
    
    def __init__(self) -> None:
        if InitApi._instance is not None:
            return True
        else:
            return self.createInstanceApi()

    # Creamos intancia de flask para crea una api
    def createInstanceApi():
        app = Flask(__name__)

        # Usamos CORS para evitar peticiones de otros dominios que no sean nuestra paginas
        CORS(app, supports_credentials=True, origins=["https://main.d2gljrmlfnpv4z.amplifyapp.com"])

        # Agregamos rutas que van a estar siendo expuestas en nuestra api
        app.register_blueprint(api_auth, url_prefix='/auth/user')

        @app.route('/', methods=['GET'])
        def home():
            return "API is running", 200

        # Retornamos la instancia
        return app

        


