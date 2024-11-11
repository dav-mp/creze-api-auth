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
    
    response = make_response(controller.userLogin( data ))

    csrf_token = CSRFProvider.generateCsrfToken()

    response.set_cookie('csrf_token', csrf_token, httponly=True, secure=True, samesite='Strict')

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
        
