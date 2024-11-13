from flask import Blueprint, request, make_response
from src.config import SdkAws
from src.controller import AuthController
from src.service import AuthService, AuthServiceProvider

from src.config import CSRFProvider

api_auth = Blueprint('api_auth', __name__)

# ID
sdk = SdkAws.getInstance()
authServiceProvider = AuthServiceProvider( sdk )
service = AuthService( authServiceProvider )
controller = AuthController( service )

# TODO: buscar como aplicar el rate limit de peticiones

@api_auth.route('/userRegister', methods=['Post'])
def userRegister():
    try:
        data = request.get_json()
        return controller.userRegister( data )
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400

@api_auth.route('/userConfirm', methods=["Post"])
def userConfirm():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.userConfirm( data )

@api_auth.route('/userLogin', methods=["Post"])
def userLogin():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    
    # Suponiendo que `data` es el payload de autenticación
    response_data = controller.userLogin(data)
    response = make_response(response_data)

    print(response_data)

    if response_data[1] != 200:
        if response_data[0].get('error'):
            return response_data

    # Genera el token CSRF
    csrf_token = CSRFProvider.generateCsrfToken()

    # Agrega el token CSRF en la cookie con `httponly=True`
    response.set_cookie('csrf_token', csrf_token, httponly=True, secure=True, samesite='Strict')

    # Agrega el token CSRF en el cuerpo de la respuesta JSON
    response = make_response({
        "data": response_data,
        "csrf_token": csrf_token
    })

    return response 

@api_auth.route('/confirmMFA', methods=["Post"])
@CSRFProvider.csrf_protect
def confirmMFA():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.confirmMFA( data )   

@api_auth.route('/verifyMfaCode', methods=["Post"])
@CSRFProvider.csrf_protect
def verifyMfaCode():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.verifyMfaCode( data ) 

@api_auth.route('/userLogout', methods=["Post"])
@CSRFProvider.csrf_protect
def userLogout():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.userLogout( data )     
        
