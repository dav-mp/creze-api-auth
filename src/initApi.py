from flask import Flask

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

    def createInstanceApi():
        app = Flask(__name__)

        app.register_blueprint(api_auth, url_prefix='/auth/user')

        return app

        


