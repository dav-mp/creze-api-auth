from src.domain.dto import UserRegisterDTO
from src.service.authServiceProvider import AuthServiceProvider

class AuthService: 


    def __init__(self, authServiceProvider: AuthServiceProvider ) -> None:
        self.authServiceProvider = authServiceProvider
        pass

    def userRegister( self, user: UserRegisterDTO ):

        self.authServiceProvider.getEnvsBySdk()
        pass

