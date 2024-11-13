from src.domain.dto import UserRegisterDTO, userConfirmDTO, UserLoginDTO, ConfirmMFADTO, VerifyMFACodeDTO, UserLogoutDTO
from src.service.authServiceProvider import AuthServiceProvider

# Clase de tipo servicio que nos ayuda a conectarnos con nuestro proveedor para hacer un flujo de auth
# Si se trabajara con un ORM aqui mismo se haria la logica de extraccion de datos, sin necesidad de un AuthServiceProvider

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

    def userLogin( self, data: UserLoginDTO ):

        login = self.authServiceProvider.userLogin( data )

        return login

    def confirmMFA( self, data: ConfirmMFADTO):
        
        confirmMfa = self.authServiceProvider.confirmMFA( data )

        return confirmMfa
    
    def verifyMfaCode( self, data: VerifyMFACodeDTO ):
        
        mfaVerify = self.authServiceProvider.verifyMfaCode( data )

        return mfaVerify
    
    def userLogout( self, session: UserLogoutDTO ):

        logout = self.authServiceProvider.userLogout( session )

        return logout
