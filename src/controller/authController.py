from src.service import AuthService
from src.domain.dto import UserRegisterDTO, UserConfirmDTO, UserLoginDTO, ConfirmMFADTO, VerifyMFACodeDTO


class AuthController:

    def __init__(self, service: AuthService) -> None:
        self.service = service

    def userRegister( self, data ):

        [ error, dataDto ] = UserRegisterDTO.createDTO( data )
        
        print('ErrorDto', error)

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

        [ error, dataDto ] = UserConfirmDTO.createDTO( data )

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

        [ error, dataDto ] = UserLoginDTO.createDTO( data )

        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.userLogin( dataDto )
    
    def confirmMFA( self, data ):

        [ error, dataDto ] = ConfirmMFADTO.createDTO( data )

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

        [ error, dataDto ] = VerifyMFACodeDTO.createDTO( data )

        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        return self.service.verifyMfaCode( dataDto )




