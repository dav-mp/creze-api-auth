from src.service import AuthService
from src.domain.dto import UserRegisterDTO


class AuthController:

    def __init__(self, service: AuthService) -> None:
        self.service = service

    def userRegister( self, data ):

        [ error, dataDto ] = UserRegisterDTO.createDTO( data )
        
        if( error ):
            return {
                "fieldsError": dataDto,
                "status": {
                    "code": 400,
                    "message": "Bad request."
                }
            }, 400
        
        self.service.userRegister( dataDto )


        print(error)
        print(dataDto)


        print("Andrey puto")

        return "Andrey Puto"