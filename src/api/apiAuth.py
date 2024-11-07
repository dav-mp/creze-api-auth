from flask import Blueprint, request

from src.config import SdkAws
from src.controller import AuthController
from src.service import AuthService, AuthServiceProvider

api_auth = Blueprint('api_auth', __name__)

# ID
sdk = SdkAws.getInstance()
authServiceProvider = AuthServiceProvider( sdk )
service = AuthService( authServiceProvider )
controller = AuthController( service )


@api_auth.route('/userRegister', methods=['Post'])
def userRegister():
    data = request.get_json()
    return controller.userRegister( data )