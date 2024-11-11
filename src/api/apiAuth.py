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
    return controller.userLogin( data )

@api_auth.route('/confirmMFA', methods=["Post"])
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
def verifyMfaCode():
    try:
        data = request.get_json()
    except Exception as e:
        print('no tiene json')
        return {
            "error":"there is no data"
        }, 400
    return controller.verifyMfaCode( data ) 

    
        
