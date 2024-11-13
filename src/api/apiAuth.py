from flask import Blueprint, request, make_response
from src.config import SdkAws
from src.controller import AuthController
from src.service import AuthService, AuthServiceProvider

from src.config import CSRFProvider

# Creamos la ruta de nuestra api 
api_auth = Blueprint('api_auth', __name__)

# ID
# Utilizamos inyeccion de dependencias para mayor escalabilidad y separacion de responsabilidad
sdk = SdkAws.getInstance() # SKD de aws para interactuar con microservicios de AWS
authServiceProvider = AuthServiceProvider( sdk ) # Servicio que utiliza un proveedor para auth
service = AuthService( authServiceProvider ) # Servicio que se usa para hacer las funcionalidades de Auth (Login, Register, Logout)
controller = AuthController( service ) # Controlador que se encarga de orquestar las peticiones y los flujos

# TODO: buscar como aplicar el rate limit de peticiones

@api_auth.route('/userRegister', methods=['Post'])
def userRegister():
    # Validamos que la peticion tenga un JSON
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
    
    response_data = controller.userLogin(data)
    response = make_response(response_data)

    print(response_data)

    # Validacion si hubo algun error
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
@CSRFProvider.csrf_protect # Validamos el token que provee login
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
@CSRFProvider.csrf_protect # Validamos el token que provee login
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
@CSRFProvider.csrf_protect # Validamos el token que provee login
def userLogout():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.userLogout( data )     
        
