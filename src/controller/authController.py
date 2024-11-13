from src.service import AuthService
from src.domain.dto import UserRegisterDTO, UserConfirmDTO, UserLoginDTO, ConfirmMFADTO, VerifyMFACodeDTO, UserLogoutDTO


class AuthController:

    def __init__(self, service: AuthService) -> None:
        self.service = service

    def userRegister( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = UserRegisterDTO.createDTO( data )
        
        print('ErrorDto', error)

        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.userRegister( dataDto )


    def userConfirm( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = UserConfirmDTO.createDTO( data )

        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.userConfirm( dataDto )
    
    def userLogin( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = UserLoginDTO.createDTO( data )
        
        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "error": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.userLogin( dataDto )
    
    def confirmMFA( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = ConfirmMFADTO.createDTO( data )
        
        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400

        return self.service.confirmMFA( dataDto )
    
    def verifyMfaCode( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = VerifyMFACodeDTO.createDTO( data )
        
        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.verifyMfaCode( dataDto )
    
    def userLogout( self, data ):

        # Pasamos el JSON a nuestro DTO para validar campos necesarios para procesar la info
        [ error, dataDto ] = UserLogoutDTO.createDTO( data )
        
        # Valdiamos si hay algun error en el cuerpo de la peticion
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.userLogout( dataDto )



