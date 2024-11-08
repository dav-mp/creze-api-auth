from src.domain.dto import UserRegisterDTO, userConfirmDTO
from src.service.authServiceProvider import AuthServiceProvider

class AuthService: 


    def __init__(self, authServiceProvider: AuthServiceProvider ) -> None:
        self.authServiceProvider = authServiceProvider
        pass

    def userRegister( self, user: UserRegisterDTO ):

        newUser = self.authServiceProvider.userRegister( user )

        return newUser
    
    def userConfirm( self, data: userConfirmDTO ):

        confirmation = self.authServiceProvider.userConfirm( data )

        return confirmation



