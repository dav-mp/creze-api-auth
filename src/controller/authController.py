from src.service import AuthService
from src.domain.dto import UserRegisterDTO, UserConfirmDTO


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


